import sys
from lib_carotte import *

def interrupts(irq, saved_pc, databus, csrselect, we):
	assert(irq.bus_size == 1)
	assert(saved_pc.bus_size == 32)
	assert(databus.bus_size  == 32)
	assert(csrselect.bus_size == 32)

	csrs0 = Select(20, csrselect) # kludge because of carotte
	csrs1 = Select(21, csrselect)

	IE_normal  = Mux(~csrs1 & ~csrs0 & we, Defer(32, lambda: IE), databus)
	IF_normal  = Mux(irq, Mux(~csrs1 &  csrs0 & we, Defer(32, lambda: IF), databus), Constant("0"*31 + "1"))
	IRA_normal = Mux(csrs1 & we, Defer(32, lambda: IRA), databus)
	
	IE  = Reg(Mux(Defer(1, lambda: trigger), IE_normal,  Constant("0"*32)))
	IF  = Reg(IF_normal)
	IRA = Reg(Mux(Defer(1, lambda: trigger), IRA_normal, saved_pc))

	trigger = IE[0] & IF[0]

	IE.set_as_output("IE")
	IF.set_as_output("IF")
	IRA.set_as_output("IRA")

	outreg = Mux(csrs1,
			Mux(csrs0, IE, IF),
			IRA)
	return (trigger, outreg)
