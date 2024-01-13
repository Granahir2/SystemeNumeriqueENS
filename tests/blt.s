addi x1, x0, 1		# 0
blt  x1, x0, label	# 4
nops: nop		# 8
label: addi x1, x0, 12	#12
bge x0, x0, nops	#16 Expected 0 4 8 12 16 8
