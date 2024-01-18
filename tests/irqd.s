ip: jal x0, main	 # 0
isr: lui x1, 1		 # 4
xor x0, x1, x1		 # 8
main:	xor  x1, x1, x1	 # 12
	addi x1, x0,  1  # 16
	csrrw x0, 0, x1 # IE : 20
	csrrw x0, 1, x1 # IF : 24
	nop		 # 28
	nop		 # 32
