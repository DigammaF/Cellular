
from __future__ import annotations
from dataclasses import dataclass

@dataclass
class Vec:
	x: int
	y: int

	def __hash__(self) -> int:
		return hash((self.x, self.y))

	def __add__(self, vec: Vec) -> Vec:
		return Vec(self.x + vec.x, self.y + vec.y)
