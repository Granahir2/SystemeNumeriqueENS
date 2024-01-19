addi x1, x0, 42
addi x2, x0, 2
sub  x3, x1, x2 # Do x1 - x2  (expect 40)
sll  x3, x1, x2 # Do x1 >> x2 (expect 10)
srl  x3, x1, x2 # Do x1 << x2 (expect 168)
