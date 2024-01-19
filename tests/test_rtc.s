nop # slide
csrrw x0, 1, x0 # set IF = 0
addi  x1, x0, 1
csrrw x0, 0, x1 # set EI = 1
stall: jal x0, stall
