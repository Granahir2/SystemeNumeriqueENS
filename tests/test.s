lui x1, 1 
addi x1, x1, 42
sw x1, 12(x0)
xor x1, x1, x1
lh x1, 12(x0) # Expect 4096 + 42 = 4138
