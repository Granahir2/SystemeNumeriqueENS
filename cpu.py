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

	(mux, we, ram_width, imm, imm_en, oa1, oa2, ia1, alu_opc) = decoder.decoder(instruction_ROM)

	(out1, out2, pc_out) = register_file.register_file(oa1, oa2, ia1, Defer(32, lambda: muxout), Defer(32, lambda: incr_pc))
	incr_pc, c = ripple_carry_adder(pc_out, Constant("0"*29 + "100"), Constant("0"))
	# Using carry lookahead with defer mysteriously fails (netlist references _l_0 but doesn't declare it)

	alu_in1 = Mux(imm_en, out1, imm)
	alu_in2 = out2
	alu_result, _ = alu.alu(alu_in1, alu_in2, alu_opc)	

	read_from_ram, write_to_ram = ram_interface.ram_interface(Defer(32, lambda: ramword), out1, ram_width)
	ramword = RAM(16, 32, alu_result[2:18], we, alu_result[2:18], write_to_ram)	 

	muxout = Mux(mux, alu_result, read_from_ram)

	instruction_ROM.set_as_output("iw")	
	mux.set_as_output("load")
	alu_in1.set_as_output("ALU1")
	alu_in2.set_as_output("ALU2")
	muxout.set_as_output("databus")
	pc_out.set_as_output("pc")
