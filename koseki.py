
from __future__ import annotations
from enum import Enum
from dataclasses import dataclass
from typing import Callable, Iterable, Iterator
from rich.console import Console
from rich.panel import Panel

from koseki_ops import *

def safe_get_function(code: int, library: Library) -> Function:
	return library[code] if 0 <= code < len(library) else library[0]

class ProcessStatus(Enum):
	INVALID = "invalid"
	RUNNING = "running"
	HALTED = "halted"
	WAITING = "waiting"
	SLEEPING = "sleeping"

def parse_process_status(process_status: ProcessStatus) -> int:
	match process_status:
		case ProcessStatus.INVALID: return 0
		case ProcessStatus.RUNNING: return 1
		case ProcessStatus.HALTED: return 2
		case ProcessStatus.WAITING: return 3
		case ProcessStatus.SLEEPING: return 4

@dataclass
class Process:
	_data: list[int]
	_alt_data: list[int]
	_ops: tuple[OP, ...]
	_signals: list[int]
	_head: int
	_a: int
	_b: int
	_c: int
	_status: ProcessStatus
	_parent_process: int|None

	@property
	def status(self) -> ProcessStatus:
		return self._status
	
	@status.setter
	def status(self, value: ProcessStatus):
		self._status = value
	
	@property
	def data_size(self) -> int:
		return len(self._data) + len(self._alt_data) + len(self._signals)
	
	@property
	def parent_process(self) -> int|None:
		return self._parent_process
	
	@property
	def has_signal_queued(self) -> bool:
		return len(self._signals) > 0

	@staticmethod
	def new(ops: tuple[OP, ...]) -> Process:
		return Process(
			[ ], [ ], ops, [ ], 0,
			0, 0, 0, ProcessStatus.RUNNING, None
		)

	def make_child(self, ops: tuple[OP, ...], parent_process: int) -> Process:
		return Process(
			self._data, [ ], ops, [ ], 0,
			0, 0, 0, ProcessStatus.RUNNING, parent_process
		)
	
	def on_receive_signal(self, signal: int):
		self._signals.append(signal)

	def pull_signal(self) -> int:
		return self._signals.pop(0)

	def _safe_pull_signal(self) -> int:
		return self._signals.pop(0) if self._signals else 0

	def _safe_get_op(self, key: int) -> OP:
		return self._ops[key] if 0 <= key < len(self._ops) else NoOP()

	def _safe_get_data(self) -> int:
		return self._data[-1] if self._data else 0

	def _safe_pop_data(self) -> int:
		return self._data.pop() if self._data else 0

	def run_step(self, machine: Machine, process_key: int):
		if self._head >= len(self._ops):
			self._status = ProcessStatus.HALTED
			return

		if self._head < 0:
			self._head = 0

		match self._ops[self._head]:
			case PushData(arg=value):
				self._data.append(value)

			case ConditionalOpen():
				if self._a == 0:
					level: int = 1

					while level > 0:
						self._head += 1

						if self._head >= len(self._ops):
							self._head = len(self._ops)
							break

						match self._ops[self._head]:
							case ConditionalOpen(): level += 1
							case ConditionalClose(): level -= 1

			case ConditionalClose():
				if self._a != 0:
					level: int = 1

					while level > 0:
						self._head -= 1

						if self._head < 0:
							self._head = 0
							break
			
						match self._ops[self._head]:
							case ConditionalOpen(): level -= 1
							case ConditionalClose(): level += 1

			case SetA():
				self._a = self._safe_get_data()

			case SetB():
				self._b = self._safe_get_data()

			case SetC():
				self._c = self._safe_get_data()

			case PushA():
				self._data.append(self._a)

			case PushB():
				self._data.append(self._b)

			case PushC():
				self._data.append(self._c)

			case ConstantA(arg=value):
				self._a = value

			case ConstantB(arg=value):
				self._b = value

			case ConstantC(arg=value):
				self._c = value

			case MoveA():
				self._a = self._safe_pop_data()

			case MoveB():
				self._b = self._safe_pop_data()

			case MoveC():
				self._c = self._safe_pop_data()

			case Arithmetics(arg=code):
				function = safe_get_function(code, ARITHMETICS)
				self._a = function.callback(self._a, self._b, self._c)

			case DropData():
				self._data.pop() if self._data else ...

			case SaveAlt():
				self._alt_data.append(self._data.pop()) if self._data else ...

			case LoadAlt():
				self._data.append(self._alt_data.pop()) if self._alt_data else ...

			case Halt():
				self._status = ProcessStatus.HALTED

			case SendSignal():
				machine.safe_send_signal(self._b, self._a)

			case PullSignal():
				self._a = self._safe_pull_signal()

			case SpawnProcess():
				ram = machine.safe_get_RAM(self._a)
				process = Process.new(safe_parse_RAM(ram))
				machine.spawn_process(process, self._b)

			case ReadProcess():
				self._a = parse_process_status(machine.safe_read_process(self._a))

			case ReadRAM():
				self._a = machine.safe_read_RAM(self._a, self._b)

			case WriteRAM():
				machine.safe_write_RAM(self._a, self._b, self._c)

			case CloneRAM():
				machine.safe_clone_RAM(self._a, self._b)

			case DropRAM():
				machine.safe_drop_RAM(self._a)

			case Call():
				self._status = ProcessStatus.WAITING
				ops = safe_parse_RAM(machine.safe_get_RAM(self._a))
				child = self.make_child(ops, process_key)
				machine.spawn_process(child)

			case Sleep():
				self.status = ProcessStatus.SLEEPING

			case Debug(python=python):
				print(f"{self._a} {self._b} {self._c} {self._data}")
				exec(python)

			case op: raise Exception(f"not implemented: {op}")

		self._head += 1

		if self._head >= len(self._ops):
			self._status = ProcessStatus.HALTED
			return

def safe_pop_RAM(ram: list[int]) -> int:
	return ram.pop(0) if ram else 0

def safe_get_OP_type(key: int) -> type[OP]:
	return OPS[key] if 0 <= key < len(OPS) else NoOP

def safe_parse_RAM(ram: list[int]) -> tuple[OP, ...]:
	ops: list[OP] = [ ]
	wram = ram[:]

	while wram:
		op_type = safe_get_OP_type(wram.pop(0))
		
		if op_type in (
			DropData, ConditionalOpen, ConditionalClose, SaveAlt, LoadAlt, Halt,
			SendSignal, PullSignal,
			SpawnProcess, ReadProcess,
			ReadRAM, WriteRAM, CloneRAM, DropRAM,
			SetA, SetB, SetC, PushA, PushB, PushC, MoveA, MoveB, MoveC,
			Debug
		):
			ops.append(op_type())

		if op_type in (PushData, ConstantA, ConstantB, ConstantC, Arithmetics):
			ops.append(op_type(safe_pop_RAM(wram)))

	return tuple(ops)

def parse_OPs(ops: tuple[OP, ...]) -> list[int]:
	ram: list[int] = [ ]

	for op in ops:
		if isinstance(op, (
			DropData, ConditionalOpen, ConditionalClose, SaveAlt, LoadAlt, Halt,
			SendSignal, PullSignal,
			SpawnProcess, ReadProcess,
			ReadRAM, WriteRAM, CloneRAM, DropRAM,
			SetA, SetB, SetC, PushA, PushB, PushC, MoveA, MoveB, MoveC
		)):
			ram.append(OPS.index(op.__class__))

		if isinstance(op, (PushData, ConstantA, ConstantB, ConstantC, Arithmetics)):
			ram.append(OPS.index(op.__class__))
			ram.append(op.arg)

	return ram

@dataclass
class Machine:
	_processes: dict[int, Process]
	_RAMs: dict[int, list[int]]

	@staticmethod
	def new() -> Machine:
		return Machine(
			{
				0: Process.new(tuple())
			},
			{
				0: [ ]
			}
		)
	
	def init_with(
		self, rams: dict[int, list[int]], enabled: set[int]
	):
		for key, ram in rams.items():
			self._RAMs[key] = ram
			if key in enabled: self._processes[key] = Process.new(safe_parse_RAM(ram))
	
	@property
	def data_size(self) -> int:
		return (
			sum(process.data_size for process in self._processes.values())
			+ sum(len(ram) for ram in self._RAMs.values())
		)

	def run_step(self):
		processes = { key: process for key, process in self._processes.items() }

		for key, process in processes.items():
			match process.status:
				case ProcessStatus.RUNNING:
					process.run_step(self, key)
				
				case ProcessStatus.HALTED:
					if process.parent_process is not None and process.parent_process in self._processes:
						parent = self._processes[process.parent_process]
						if parent.status == ProcessStatus.WAITING: parent.status = ProcessStatus.RUNNING

					if key != 0: del self._processes[key]

	def run(self):
		useless_steps: int = 0

		while self._processes:
			self.run_step()

			if not any(process.status == ProcessStatus.RUNNING for process in self._processes.values()):
				useless_steps += 1

			else:
				useless_steps = 0

			if useless_steps > 3:
				return

	def safe_get_process(self, key: int) -> Process:
		return self._processes[key] if key in self._processes else self._processes[0]

	def safe_get_RAM(self, key: int) -> list[int]:
		return self._RAMs[key] if key in self._RAMs else self._RAMs[0]

	def safe_read_RAM(self, ram_index: int, key: int) -> int:
		ram = self.safe_get_RAM(ram_index)
		return ram[key] if 0 <= key < len(ram) else 0
	
	def safe_write_RAM(self, ram_index: int, key: int, value: int):
		ram = self.safe_get_RAM(ram_index)
		if 0 <= key:
			while key >= len(ram): ram.append(0)
			ram[key] = value

	def safe_clone_RAM(self, ram_index: int, new_ram_index: int):
		ram = self.safe_get_RAM(ram_index)
		self._RAMs[new_ram_index] = ram[:]

	def safe_drop_RAM(self, index: int):
		if index in self._RAMs and index != 0: del self._RAMs[index]

	def safe_read_process(self, index: int) -> ProcessStatus:
		return self._processes[index].status if index in self._processes else ProcessStatus.INVALID

	def safe_send_signal(self, process_index: int, signal: int):
		self.safe_get_process(process_index).on_receive_signal(signal)

	def safe_pull_signals(self, process_index: int) -> Iterator[int]:
		if process_index in self._processes:
			process = self._processes[process_index]

			while process.has_signal_queued:
				yield process.pull_signal()

		else:
			return iter([ ])

	def spawn_process(self, process: Process, process_index: int|None = None):
		if process_index is None:
			process_index = 0
			while process_index in self._processes: process_index += 1

		self._processes[process_index] = process

	def set_RAM(self, key: int, ram: list[int]):
		self._RAMs[key] = ram
