import sys
sys.path.append("/home/salsifi/cours/di_sysnum/carotte.py")
from lib_carotte import *

from alu import alu
from alu.add_and_subtract import ripple_carry_adder
from decoder import decoder
from ram_interface import ram_interface
from register_file import register_file

def main():
	allow_ribbon_logic_operations(True)	
	#instruction_ROM = Input(32)
	
	ROM_addr = Slice(2, 18, Defer(32, lambda: pc_out)) # Since we have 32 bit words and 16 bit ROM total
	instruction_ROM = ROM(16, 32, ROM_addr)

	(mux, we, ram_width,
	imm, imm_en,
	oa1, oa2, ia1,
	alu_opc,
	pc_override_com, pc_alu, save_pc, eqsel) = decoder.decoder(instruction_ROM)

	pc_override = Mux(pc_override_com[1], pc_override_com[0], pc_override_com[2] ^ Defer(1, lambda: eq))

	(out1, out2, pc_out, eq) = register_file.register_file(oa1, oa2, ia1, Defer(32, lambda: muxout), Defer(32, lambda: incr_pc),
								pc_override, pc_alu, save_pc, eqsel)
	incr_pc, c = ripple_carry_adder(pc_out & Constant("1"*30 + "00"), Constant("0"*29 + "100"), Constant("0"))
	# Using carry lookahead with defer mysteriously fails (netlist references _l_0 but doesn't declare it)

	alu_in1 = Mux(imm_en, out1, imm)
	alu_in2 = out2
	alu_result, _ = alu.alu(alu_in1, alu_in2, alu_opc)	

	read_from_ram, write_to_ram = ram_interface.ram_interface(Defer(32, lambda: ramword), out1, ram_width, alu_result[0:2])
	ramword = RAM(16, 32, alu_result[2:18], we, alu_result[2:18], write_to_ram)	 

	muxout = Mux(mux, alu_result, read_from_ram)

	#imm_en.set_as_output("imm_en")
	alu_in1.set_as_output("alu1")
	alu_in2.set_as_output("alu2")

	mux.set_as_output("load")
	we.set_as_output("we")
	write_to_ram.set_as_output("write_to_ram")
	alu_result.set_as_output("ram_addr")
	muxout.set_as_output("databus")
	pc_out.set_as_output("pc")
