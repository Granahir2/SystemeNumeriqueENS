xor x1, x1, x1
addi x1, x0, 42
auipc x1, 1 # Expected : 4096 + (pc = 8) = 4104
