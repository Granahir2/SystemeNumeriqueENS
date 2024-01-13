addi x1, x0, 12		# 0
beq x1, x0, yes		# 4
sub x1, x1, x1		# 8
beq x1, x1, yes		#12
nops: nop		#16
yes: addi x1, x0, 10	#20
bne x0, x1, nops	#24 Expected 0 4 8 12 20 24 16
