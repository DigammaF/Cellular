
from dataclasses import dataclass
from typing import Callable

true = 1
false = 0

@dataclass
class OP:
	arg: int = 0

	def __repr__(self) -> str:
		reprs: list[str] = [ ]
		if self.arg != 0: reprs.append(str(self.arg))
		return f"{self.__class__.__name__}({", ".join(reprs)})"

class NoOP(OP): ...
class PushData(OP): ...
class DropData(OP): ...
class ConditionalOpen(OP): ...
class ConditionalClose(OP): ...
class Arithmetics(OP): ...
class SaveAlt(OP): ...
class LoadAlt(OP): ...
class Halt(OP): ...
class Call(OP): ...
class Sleep(OP): ...

class SendSignal(OP): ...
class PullSignal(OP): ...
class SpawnProcess(OP): ...
class ReadProcess(OP): ...
class ReadRAM(OP): ...
class WriteRAM(OP): ...
class CloneRAM(OP): ...
class DropRAM(OP): ...

class SetA(OP): ...
class SetB(OP): ...
class SetC(OP): ...
class PushA(OP): ...
class PushB(OP): ...
class PushC(OP): ...
class ConstantA(OP): ...
class ConstantB(OP): ...
class ConstantC(OP): ...
class MoveA(OP): ...
class MoveB(OP): ...
class MoveC(OP): ...

@dataclass
class Debug(OP):
	python: str = "..."

OPS: tuple[type[OP], ...] = (
	NoOP, PushData, DropData,
	ConditionalOpen, ConditionalClose,
	Arithmetics,
	SaveAlt, LoadAlt,
	Halt, Call,
	SendSignal, PullSignal,
	SpawnProcess, ReadProcess,
	ReadRAM, WriteRAM, CloneRAM, DropRAM,
	SetA, SetB, SetC, PushA, PushB, PushC,
	ConstantA, ConstantB, ConstantC,
	MoveA, MoveB, MoveC
)

@dataclass
class Function:
	callback: Callable[[int, int, int], int]
	name: str

type Library = tuple[Function, ...]

ARITHMETICS: Library = (
	Function(lambda a, b, c: a, "Identity"),
	Function(lambda a, b, c: a + b, "Addition"),
	Function(lambda a, b, c: a*b, "Multiplication"),
	Function(lambda a, b, c: a - b, "Substraction"),
	Function(lambda a, b, c: 999 if b == 0 else int(a/b), "Division"),
	Function(lambda a, b, c: a % b, "Modulo"),

	Function(lambda a, b, c: true, "Constant true"),
	Function(lambda a, b, c: int(a > b), ">"),
	Function(lambda a, b, c: int(a >= b), ">="),
	Function(lambda a, b, c: int(a < b), "<"),
	Function(lambda a, b, c: int(a <= b), "<="),
	Function(lambda a, b, c: int(a == b), "=="),
	Function(lambda a, b, c: int(a != b), "!=")
)

def get_function(name: str, library: Library = ARITHMETICS) -> int:
	for key, function in enumerate(library):
		if function.name == name:
			return key

	raise Exception(f"couldn't find function {name}")