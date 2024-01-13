jal x1, label		# 0
nops: nop		# 4
nop 			# 8
label: xor x1, x1, x1   #12
jal x1, nops 		#16
nop 			#20 Expect : 0 12 16 4 8 12
