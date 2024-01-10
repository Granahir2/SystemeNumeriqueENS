import sys
from lib_carotte import *

def sgnextend12(x):
#	assert(x.bus_size == 12)
	return x + Mux(x[11], Constant("0"*20), Constant("1"*20))

def decode_aluopc(inner_enc):
	assert(inner_enc.bus_size == 4)
	a = (inner_enc[2] & inner_enc[0]) | (~inner_enc[0] & ~inner_enc[1])
	b = inner_enc[0]
	c = ~((~inner_enc[0] & ~inner_enc[2]) | (inner_enc[0] & inner_enc[1]))
	r = c + b + a
	return Mux(inner_enc[3], r, Constant("010"))

def decoder(iw):
	assert(iw.bus_size == 32)
	
	is_load   = ~iw[2] & ~iw[4] & ~iw[5] # We don't support anything else *now*
	is_store  = ~iw[2] & ~iw[4] &  iw[5]
	is_arithi = ~iw[2] &  iw[4] & ~iw[5]
	is_arith  = ~iw[2] &  iw[4] &  iw[5]
	is_lui    =  iw[2] 

	mux 	  = is_load
	we  	  = is_store
	ram_width = iw[12:15]
	regs_in   = Mux(is_store, iw[7:12], Constant("00000"))
	regs_out1 = iw[20:25]
	regs_out2 = iw[15:20]
	imm_en    = ~is_arith
	imm	  = Mux(is_lui,
			sgnextend12(Mux(is_store, iw[20:32], iw[7:12] + iw[25:32])),
			Constant("0"*12) + iw[12:32])
	alu_opc_internal = Mux(is_arith | is_arithi,
				Constant("0000"),
				(is_arith & iw[30]) + iw[12:15])
	alu_opc = decode_aluopc(alu_opc_internal)

	return (mux, we, ram_width,
		imm, imm_en,
		regs_out1, regs_out2, regs_in,
		alu_opc)

#def main():
#	allow_ribbon_logic_operations(True)

#	instruction_word = Input(32)
#	(mux, we, ram_width,
#	 imm, imm_en,
#	 regs_out1, regs_out2, regs_in,
#	 alu_opc) = decoder(instruction_word)
#
#	mux.set_as_output("mux")
#	we.set_as_output("we")
#	ram_width.set_as_output("width")
#	imm.set_as_output("imm")
#	imm_en.set_as_output("imm_en")
#	regs_out1.set_as_output("reg1")
#	regs_out2.set_as_output("reg2")
#	regs_in.set_as_output("regd")
#	alu_opc.set_as_output("alu")
