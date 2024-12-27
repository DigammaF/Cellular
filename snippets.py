
from koseki_ops import *

def primes():
	IS_PRIME: int = 0
	is_prime = (
		SetC(),
		ConstantA(true),
		ConditionalOpen(),

		SetA(), ConstantB(1), Arithmetics(get_function("Substraction")),
		DropData(), PushA(),

		PushC(), MoveA(), SetB(), Arithmetics(get_function("Modulo")),
		ConstantB(0), Arithmetics(get_function("==")),
		ConditionalOpen(),
		DropData(), ConstantA(false), PushA(), Halt(),
		ConditionalClose(),

		SetA(), ConstantB(2), Arithmetics(get_function("!=")),
		ConditionalClose(),
		DropData(), PushData(true),
	)
	main_ops = (
		PushData(2),
		ConstantA(true),
		ConditionalOpen(),

		SetA(), ConstantB(1), Arithmetics(get_function("Addition")),
		DropData(), PushA(),

		PushA(), ConstantA(IS_PRIME), Call(),
		MoveA(),
		ConditionalOpen(),
		SetA(), ConstantB(0), SendSignal(),
		ConstantA(false),
		ConditionalClose(),

		SetA(), ConstantB(100), Arithmetics(get_function("<")),
		ConditionalClose(),
		Debug(),
	)
