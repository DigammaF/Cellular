

from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from functools import reduce
from typing import Self

from vec import Vec

class Material(Enum):
	# Metals
	IRON = "Iron"
	COPPER = "Copper"
	GOLD = "Gold"
	SILVER = "Silver"
	PLATINUM = "Platinum"
	ALUMINUM = "Aluminum"
	TITANIUM = "Titanium"
	NICKEL = "Nickel"
	ZINC = "Zinc"
	LEAD = "Lead"

	# Precious stones
	DIAMOND = "Diamond"
	RUBY = "Ruby"
	SAPPHIRE = "Sapphire"
	EMERALD = "Emerald"
	AMETHYST = "Amethyst"
	TOPAZ = "Topaz"
	OPAL = "Opal"

	# Industrial minerals
	QUARTZ = "Quartz"
	FELDSPAR = "Feldspar"
	MICA = "Mica"
	CALCITE = "Calcite"
	GYPSUM = "Gypsum"
	FLUORITE = "Fluorite"
	TALC = "Talc"
	HALITE = "Halite"

	# Alloys
	STEEL = "Steel"
	BRONZE = "Bronze"
	BRASS = "Brass"
	INVAR = "Invar"
	DURALUMIN = "Duralumin"

	# Organic materials
	WOOD = "Wood"
	AMBER = "Amber"
	PEARL = "Pearl"

	# Synthetic materials
	PLASTIC = "Plastic"
	POLYCARBONATE = "Polycarbonate"
	ACRYLIC = "Acrylic"
	POLYETHYLENE = "Polyethylene"
	POLYPROPYLENE = "Polypropylene"

	# Ceramics and glasses
	CERAMIC = "Ceramic"
	PORCELAIN = "Porcelain"
	GLASS = "Glass"
	OBSIDIAN = "Obsidian"

	# Composite materials
	CONCRETE = "Concrete"
	CARBON_FIBER = "Carbon Fiber"
	FIBERGLASS = "Fiberglass"

	# Miscellaneous
	CHARCOAL = "Charcoal"
	COAL = "Coal"
	GRAPHITE = "Graphite"
	ASBESTOS = "Asbestos"

MATERIALS: tuple[Material, ...] = tuple(Material)

class Shape(Enum):
	# Basic shapes
	CUBE = "Cube"
	SPHERE = "Sphere"
	CONE = "Cone"
	CYLINDER = "Cylinder"
	PYRAMID = "Pyramid"
	TETRAHEDRON = "Tetrahedron"
	HEXAHEDRON = "Hexahedron"
	OCTAHEDRON = "Octahedron"
	DODECAHEDRON = "Dodecahedron"
	ICOSAHEDRON = "Icosahedron"

	# Prisms
	TRIANGULAR_PRISM = "Triangular Prism"
	RECTANGULAR_PRISM = "Rectangular Prism"
	PENTAGONAL_PRISM = "Pentagonal Prism"
	HEXAGONAL_PRISM = "Hexagonal Prism"
	HEPTAGONAL_PRISM = "Heptagonal Prism"
	OCTAGONAL_PRISM = "Octagonal Prism"

	# Antiprisms
	TRIANGULAR_ANTIPRISM = "Triangular Antiprism"
	PENTAGONAL_ANTIPRISM = "Pentagonal Antiprism"
	HEXAGONAL_ANTIPRISM = "Hexagonal Antiprism"

	# Platonic solids
	REGULAR_TETRAHEDRON = "Regular Tetrahedron"
	REGULAR_HEXAHEDRON = "Regular Hexahedron"
	REGULAR_OCTAHEDRON = "Regular Octahedron"
	REGULAR_DODECAHEDRON = "Regular Dodecahedron"
	REGULAR_ICOSAHEDRON = "Regular Icosahedron"

	# Archimedean solids
	TRUNCATED_TETRAHEDRON = "Truncated Tetrahedron"
	TRUNCATED_CUBE = "Truncated Cube"
	TRUNCATED_OCTAHEDRON = "Truncated Octahedron"
	TRUNCATED_DODECAHEDRON = "Truncated Dodecahedron"
	TRUNCATED_ICOSAHEDRON = "Truncated Icosahedron"
	SNUB_CUBE = "Snub Cube"
	SNUB_DODECAHEDRON = "Snub Dodecahedron"

	# Other shapes
	TORUS = "Torus"
	ELLIPSOID = "Ellipsoid"
	HYPERBOLOID = "Hyperboloid"
	PARABOLOID = "Paraboloid"
	SPHEROID = "Spheroid"
	CAPSULE = "Capsule"
	FRUSTUM = "Frustum"
	TRUNCATED_CONE = "Truncated Cone"
	TRUNCATED_PYRAMID = "Truncated Pyramid"

	# Complex shapes
	RHOMBIC_DODECAHEDRON = "Rhombic Dodecahedron"
	DELTOIDAL_ICOSITETRAHEDRON = "Deltoidal Icositetrahedron"
	ZONOHEDRON = "Zonohedron"

SHAPES: tuple[Shape, ...] = tuple(Shape)

class ChemicalElement(Enum):
	# Alkali metals
	HYDROGEN = "Hydrogen (H)"
	LITHIUM = "Lithium (Li)"
	SODIUM = "Sodium (Na)"
	POTASSIUM = "Potassium (K)"
	RUBIDIUM = "Rubidium (Rb)"
	CESIUM = "Cesium (Cs)"
	FRANCIUM = "Francium (Fr)"

	# Alkaline earth metals
	BERYLLIUM = "Beryllium (Be)"
	MAGNESIUM = "Magnesium (Mg)"
	CALCIUM = "Calcium (Ca)"
	STRONTIUM = "Strontium (Sr)"
	BARIUM = "Barium (Ba)"
	RADIUM = "Radium (Ra)"

	# Transition metals
	SCANDIUM = "Scandium (Sc)"
	TITANIUM = "Titanium (Ti)"
	VANADIUM = "Vanadium (V)"
	CHROMIUM = "Chromium (Cr)"
	MANGANESE = "Manganese (Mn)"
	IRON = "Iron (Fe)"
	COBALT = "Cobalt (Co)"
	NICKEL = "Nickel (Ni)"
	COPPER = "Copper (Cu)"
	ZINC = "Zinc (Zn)"

	# Post-transition metals
	ALUMINUM = "Aluminum (Al)"
	GALLIUM = "Gallium (Ga)"
	INDIUM = "Indium (In)"
	TIN = "Tin (Sn)"
	LEAD = "Lead (Pb)"
	BISMUTH = "Bismuth (Bi)"

	# Metalloids
	BORON = "Boron (B)"
	SILICON = "Silicon (Si)"
	GERMANIUM = "Germanium (Ge)"
	ARSENIC = "Arsenic (As)"
	ANTIMONY = "Antimony (Sb)"
	TELLURIUM = "Tellurium (Te)"

	# Nonmetals
	CARBON = "Carbon (C)"
	NITROGEN = "Nitrogen (N)"
	OXYGEN = "Oxygen (O)"
	PHOSPHORUS = "Phosphorus (P)"
	SULFUR = "Sulfur (S)"
	SELENIUM = "Selenium (Se)"

	# Halogens
	FLUORINE = "Fluorine (F)"
	CHLORINE = "Chlorine (Cl)"
	BROMINE = "Bromine (Br)"
	IODINE = "Iodine (I)"
	ASTATINE = "Astatine (At)"

	# Noble gases
	HELIUM = "Helium (He)"
	NEON = "Neon (Ne)"
	ARGON = "Argon (Ar)"
	KRYPTON = "Krypton (Kr)"
	XENON = "Xenon (Xe)"
	RADON = "Radon (Rn)"

	# Lanthanides
	LANTHANUM = "Lanthanum (La)"
	CERIUM = "Cerium (Ce)"
	PRASEODYMIUM = "Praseodymium (Pr)"
	NEODYMIUM = "Neodymium (Nd)"
	PROMETHIUM = "Promethium (Pm)"
	SAMARIUM = "Samarium (Sm)"
	EUROPIUM = "Europium (Eu)"
	GADOLINIUM = "Gadolinium (Gd)"
	TERBIUM = "Terbium (Tb)"
	DYSPROSIUM = "Dysprosium (Dy)"
	HOLMIUM = "Holmium (Ho)"
	ERBIUM = "Erbium (Er)"
	THULIUM = "Thulium (Tm)"
	YTTERBIUM = "Ytterbium (Yb)"
	LUTETIUM = "Lutetium (Lu)"

	# Actinides
	ACTINIUM = "Actinium (Ac)"
	THORIUM = "Thorium (Th)"
	PROTACTINIUM = "Protactinium (Pa)"
	URANIUM = "Uranium (U)"
	NEPTUNIUM = "Neptunium (Np)"
	PLUTONIUM = "Plutonium (Pu)"
	AMERICIUM = "Americium (Am)"
	CURIUM = "Curium (Cm)"
	BERKELIUM = "Berkelium (Bk)"
	CALIFORNIUM = "Californium (Cf)"
	EINSTEINIUM = "Einsteinium (Es)"
	FERMIUM = "Fermium (Fm)"
	MENDELEVIUM = "Mendelevium (Md)"
	NOBELIUM = "Nobelium (No)"
	LAWRENCIUM = "Lawrencium (Lr)"

CHEMICAL_ELEMENTS: tuple[ChemicalElement, ...] = tuple(ChemicalElement)

def is_prime(n: int, /) -> bool:
	if n < 2: return False

	for k in range(2, n):
		if n % k == 0: return False

	return True

@dataclass
class Natural:
	n: int
	primes: set[int]

	@classmethod
	def from_primes(cls, primes: set[int]) -> Self:
		return cls(reduce(lambda x, y: x*y, primes), primes)

	@classmethod
	def from_n(cls, n: int) -> Self:
		return cls(n, set(k for k in range(2, n + 1) if is_prime(k)))

	def __mul__(self, natural: Natural) -> Natural:	
		return Natural(
			self.n * natural.n,
			self.primes | natural.primes
		)

	def __str__(self) -> str:
		return f"natural {self.n}"

	def __hash__(self) -> int:
		return self.n

class Matter(Natural):
	def __str__(self) -> str:
		try:
			return str(MATERIALS[self.n])

		except KeyError:
			return f"matter({self.n})"

class WaveLength(Natural):
	def __str__(self) -> str:
		return f"wavelength({self.n})"

@dataclass
class Compound:
	energy: int
	content: dict[Matter, int]

	@classmethod
	def new(cls) -> Self:
		return cls(0, { })

	def get_amount(self, material: Matter) -> int:
		return self.content.get(material, 0)

	def add(self, material: Matter, amount: int):
		self.content[material] = self.content.get(material, 0) + amount

	def rem(self, material: Matter, amount: int) -> int:
		actual_amount = min(amount, self.content.get(material, 0))
		self.content[material] = self.content.get(material, 0) - actual_amount
		return actual_amount

@dataclass
class Wave:
	energy: int
	wavelength: WaveLength
	velocity: Vec

@dataclass
class Part:
	compound: Compound
	shape: Shape
	external: bool = False

	@classmethod
	def new(cls) -> Self:
		return cls(Compound.new(), Shape.CUBE)

	def update(self, world: World, unit: Unit): ...

@dataclass
class Unit:
	body: Part
	parts: list[Part]
	velocity: Vec

	@classmethod
	def new(cls) -> Self:
		return cls(Part.new(), [ ], Vec(0, 0))

	def update(self, world: World):
		for part in self.parts[:]:
			part.update(world, self)

@dataclass
class Place:
	compount: Compound
	units: list[Unit]

class System:
	def update(self, world: World): ...

@dataclass
class World:
	units: list[Unit]
	map: dict[Vec, Place]
	systems: list[System]

	def update(self):
		for unit in self.units:
			unit.update(self)

		for system in self.systems:
			system.update(self)

	def make_unit(self) -> Unit:
		unit = Unit.new()
		self.units.append(unit)
		return unit

	def rem_unit(self, unit: Unit):
		self.units.remove(unit)
