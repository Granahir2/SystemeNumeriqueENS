from lib_carotte import *

def sgn_extend32(x):
	assert(x.bus_size < 32)
	z = Constant("0"*(32 - x.bus_size))
	o = Constant("1"*(32 - x.bus_size))
	return x + Mux(x[x.bus_size - 1], z, o)

def swap_lohi(x):
	assert(x.bus_size % 2 == 0)
	n = x.bus_size
	return Concat(Slice(n//2,n,x), Slice(0,n//2,x))

def ram_interface(from_ram, from_cpu, width, offset): # TODO support not word-aligned accesses on 16-bit, 8-bit addresses
	# This ensures that in ram_cycled1, the correct (sub-)word is in the low bits. This assumes accesses are naturally-aligned
	ram_cycled0 = Mux(Select(1, offset), from_ram, swap_lohi(from_ram))
	ram_cycled1 = Concat(
			Mux(Select(0, offset), Slice(0, 16, ram_cycled0), swap_lohi(Slice(0, 16, ram_cycled0))),
			Slice(16, 32, ram_cycled0))

	to_cpu = Mux(Select(0, width), Mux(Select(1, width), sgn_extend32(Slice(0, 8, ram_cycled1)), ram_cycled1), sgn_extend32(Slice(0, 16, ram_cycled1)))
	
	ram_patched = Mux(Select(0, width),
			Mux(Select(1, width), Concat(Slice(0, 8, from_cpu), Slice(8, 32, ram_cycled1)), from_cpu),
			Concat(Slice(0, 16, from_cpu), Slice(16, 32, ram_cycled1)))
	
	# We need to undo the cycling to get back the original word 
	ram_uncycled = Concat(
			Mux(Select(0, offset), Slice(0, 16, ram_patched), swap_lohi(Slice(0, 16, ram_patched))),
			Slice(16, 32, ram_patched))
	to_ram = Mux(Select(1, offset), ram_uncycled, swap_lohi(ram_uncycled))

	return (to_cpu, to_ram)
