# x30: second
# x29: minute
# x28: hour
# x27: day
# x26: month
# x25: year
# x24: year % 400
# x23: year % 100
# x22: year % 4
# x21: encode the number of days in each month
# TODO: modify the number 
addi x21, x21, 112 # the decimal value of 101011010101 (1 for 31 days and 0 for 30 days)
# x20: used for constant (e.g. 60, 24, 12, 400, 100, 4, ...)
# x19: whether it is a leap or not

beq x0, x0, WHILE
WHILE:
xor x1, x1, x1
lui x1, 1 # address to read the clock bit ( = 4096)
lb x2, x1 # read the clock bit from ram
xor x20, x20, x20 # x20 <- 0
beq x2, x20, WHILE # if the clock bit is off, repeat

# increase second
addi x30, x30, 1
xor x20, x20, x20
addi x20, x20, 60 # x20 <- 60
bne x30, x20, OUTPUT # output and loop
xor x30, x30, x30

# increase minute
addi x29, x29, 1
xor x20, x20, x20
addi x20, x20, 60 # x20 <- 60
bne x29, x20, OUTPUT # output and loop
xor x29, x29, x29

# increase hour
addi x28, x28, 1
xor x20, x20, x20
addi x20, x20, 24 # x20 <- 24
bne x28, x20, OUTPUT # output and loop
xor x28, x28, x28

# increase day
addi x27, x27, 1
# divide cases
xor x20, x20, x20
addi x20, x20, 1
bne x26, x20, OTHER_MONTHS
# Deal with February
xor x19, x19, x19 # x19 <- 0
beq x24, x0, LEAP_YEAR # branch if year % 400 == 0
beq x22, x0, YEAR_MOD_4 # branch if year % 4 == 0
beq x0, x0, UPDATE_FEBRUARY # otherwise not a leap year, just branch to update
#
YEAR_MOD_4:
beq x23, x0, UPDATE_FEBRUARY # if year % 4 == 0 and year % 100 == 0
beq x0, x0, LEAP_YEAR # if year % 4 == 0 and year % 100 != 0
#
LEAP_YEAR:
xori x19, x19, 1 # x19 <- 1
beq x0, x0, UPDATE_FEBRUARY
#
UPDATE_FEBRUARY:
addi x20, x19, 28 # 28 + whether it is a leap year
bne x27, x20, OUTPUT
beq x0, x0, CON
# Deal with other months
OTHER_MONTHS: 
addi x1, x21, 0 # x1 <- x21
srl x1, x1, x26 # get encode bit
andi x1, x1, 1 # corresponding to the month
xor x20, x20, x20
addi x20, x20, 30 # x20 <- 30
add x2, x1, x20 # x2 <- 30 + encode bit
bne x27, x2, OUTPUT
xor x27, x27, x27
beq x0, x0, CON

CON:
# increase year
addi x26, x26, 1
xor x20, x20, x20
addi x20, x20, 12 # x20 <- 12
bne x26, x20, OUTPUT # output and loop
xor x26, x26, x26

# increase year
addi x25, x25, 1
# update year % 400
addi x24, x24, 1
xor x20, x20, x20 
addi x20, x20, 400 # x20 <- 400
bne x24, x20, UPDATE_YEAR100
xor x24, x24, x24
beq x0, x0, UPDATE_YEAR100
# update year % 100
UPDATE_YEAR100:
addi x23, x23, 1
xor x20, x20, x20
addi x20, x20, 100 # x20 <- 100
bne x23, x20, UPDATE_YEAR4
xor x23, x23, x23
beq x0, x0, UPDATE_YEAR4
# update year % 4
UPDATE_YEAR4:
addi x22, x22, 1
xor x20, x20, x20
addi x20, x20, 4 # x20 <- 4
bne x22, x20, OUTPUT
xor x22, x22, x22
beq x0, x0, OUTPUT

# output to ram and loop
OUTPUT:
sb x30, 0(x0)
sb x29, 1(x0)
sb x28, 2(x0)
sb x27, 3(x0)
sb x26, 4(x0)
sw x25, 8(x0)
beq x0, x0, WHILE
