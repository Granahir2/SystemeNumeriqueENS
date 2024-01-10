import sys
sys.path.append("/home/salsifi/cours/di_sysnum/carotte.py")
from lib_carotte import *

from alu import alu
from decoder import decoder
from ram_interface import ram_interface
from register_file import register_file

def main():
	allow_ribbon_logic_operations(True)
	
	instruction_ROM = Input(32)
	
	ROM_addr = Slice(2, 18, Defer(32, lambda: pc_out)) # Since we have 32 bit words and 16 bit ROM total
	#instruction_ROM = ROM(16, 32, ROM_addr)


	# data in is not wired because it creates combinatorial loops ?!
	(mux, we, ram_width, imm, imm_en, oa1, oa2, ia1, alu_opc) = decoder.decoder(instruction_ROM)
	(out1, out2, pc_out) = register_file.register_file(oa1, oa2, ia1, Defer(32, lambda: muxout), Defer(32, lambda: pc_out))
	# TODO For now, PC doesn't increment ! (Instructions are hand-fed)
	
	out1 = Constant("0"*32)
	out2 = Constant("0"*32)
	pc_out = Constant("0"*32)

	alu_in1 = Mux(imm_en, out1, imm)
	alu_in2 = out2
	alu_result, _ = alu.alu(alu_in1, alu_in2, alu_opc)	

	read_from_ram, write_to_ram = ram_interface.ram_interface(Defer(32, lambda: ramword), out1, ram_width)
	ramword = RAM(16, 32, alu_result[2:18], we, alu_result[2:18], write_to_ram)	 

	muxout = Mux(mux, alu_result, read_from_ram) # RAM is hardwired to 0 for now


	oa1.set_as_output("oa1")
	oa2.set_as_output("oa2")
	ia1.set_as_output("ia1")
	mux.set_as_output("mux")
	we.set_as_output("we")
	ram_width.set_as_output("raw_width")
	imm.set_as_output("imm")
	imm_en.set_as_output("imm_en")

	alu_result.set_as_output("aluout")
	muxout.set_as_output("databus")
