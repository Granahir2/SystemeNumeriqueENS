import sys
from lib_carotte import *

def sgn_extend32(x):
	assert(x.bus_size < 32)
	z = Constant("0"*(32 - x.bus_size))
	o = Constant("1"*(32 - x.bus_size))
	return x + Mux(x[x.bus_size - 1], z, o)

def decode_imms(iw):
	i = sgn_extend32(iw[20:32])
	s = sgn_extend32(iw[7:12] + iw[25:32])
	b = sgn_extend32(Constant("0") + iw[8:12] + iw[25:31] + iw[7] + iw[31])
	u = Constant("0"*12) + iw[12:32]
	j = sgn_extend32(Constant("0") + iw[21:31] + iw[20] + iw[12:20]+ iw[31])
	return (i,s,b,u,j)

def decode_aluopc(inner_enc):
	assert(inner_enc.bus_size == 4)
	a = (inner_enc[2] & inner_enc[0]) | (~inner_enc[0] & ~inner_enc[1])
	b = inner_enc[0]
	c = ~((~inner_enc[0] & ~inner_enc[2]) | (inner_enc[0] & inner_enc[1]))
	r = c + b + a
	return Mux(inner_enc[3], r, Constant("010"))

def decoder(iw):
	assert(iw.bus_size == 32)
	
	# Refer to p. 129 of RISCV docs
	is_load   = ~iw[2] & ~iw[3] & ~iw[4] & ~iw[5] & ~iw[6]
	is_store  = ~iw[2] & ~iw[3] & ~iw[4] &  iw[5] & ~iw[6]	
	is_arithi = ~iw[2] & ~iw[3] &  iw[4] & ~iw[5] & ~iw[6]
	is_arith  = ~iw[2] & ~iw[3] &  iw[4] &  iw[5] & ~iw[6]
	is_lui    =  iw[2] & ~iw[3] &  iw[4] &  iw[5] & ~iw[6] 
	is_auipc  =  iw[2] & ~iw[3] &  iw[4] & ~iw[5] & ~iw[6]
	is_jal    =  iw[2] &  iw[3] & ~iw[4] &  iw[5] &  iw[6]
	is_jalr   =  iw[2] & ~iw[3] & ~iw[4] &  iw[5] &  iw[6]
	is_branch = ~iw[2] & ~iw[3] & ~iw[4] &  iw[5] &  iw[6]

	mux 	  = is_load
	we  	  = is_store
	ram_width = iw[12:15]

	regs_in   = Mux(is_store | is_branch, iw[7:12], Constant("00000"))
	regs_out1 = iw[20:25]
	regs_out2 = iw[15:20]

	(i,s,b,u,j) = decode_imms(iw)
	imm_en    = ~is_arith
	imm	  = Mux(is_lui | is_auipc,
			Mux(is_store,
				Mux(is_jal,
					Mux(is_branch, i, b),
					j),
				s),
			u)
	
	alu_opc_internal = Mux(is_arith | is_arithi,
				Constant("0000"), # add
				(is_arith & iw[30]) + iw[12:15])
	alu_opc = decode_aluopc(alu_opc_internal)

	# pcoc[1] = do we branch conditionally ? pcoc[0] = do we branch unconditionally ? pcoc[2] = is the condition inverted
	pc_override_com = (is_jal | is_jalr) + is_branch + iw[12]
	pc_alu	    = is_auipc | is_jal | is_branch	
	save_pc     = is_jal | is_jalr
	eqsel	    = iw[14] # All LT are *unsigned*

	return (mux, we, ram_width,
		imm, imm_en,
		regs_out1, regs_out2, regs_in,
		alu_opc,
		pc_override_com, pc_alu, save_pc, eqsel)

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
