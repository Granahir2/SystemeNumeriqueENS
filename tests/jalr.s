jalr x1, 8(x0)     #  0
xor x1, x1, x1     #  4
label: nop         #  8
jalr x0, 0(x1)     # 12 Expected : 0 8 12 4
