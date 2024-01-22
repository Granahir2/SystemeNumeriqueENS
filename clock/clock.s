# x30: second
# x29: minute
# x28: hour
# x27: day
# x26: month
# x25: year
# x24: year % 400 NOT USED ANYMORE
# x23: year % 100
# x22: year % 4
# x20: used for constant (e.g. 60, 24, 12, 400, 100, 4, ...)
# x19: whether the year is leap or not


# x3 return address. All other : scratch registers, caller saved

jal x0, init
WHILE: csrrw x0, 1, x0 # Reset IF. Note IE = 0 here

# TODO: Load the time for the clock
# x21: encode the number of days in each month
# 0xAD5: the hexadecimal value of 1010 1101 0101 (1 for 31 days and 0 for 30 days)
addi x21, x0, -1323

# increase second
addi x30, x30, 1
addi x20, x0, 60 # x20 <- 60
bne x30, x20, OUTPUT # output and loop
xor x30, x30, x30

# increase minute
addi x29, x29, 1
addi x20, x0, 60 # x20 <- 60
bne x29, x20, OUTPUT # output and loop
xor x29, x29, x29

# increase hour
addi x28, x28, 1
addi x20, x0, 24 # x20 <- 24
bne x28, x20, OUTPUT # output and loop
xor x28, x28, x28

# increase day
addi x27, x27, 1
# divide cases
addi x20, x0, 1
bne x26, x20, OTHER_MONTHS
# Deal with February
xor x19, x19, x19 # x19 <- 0, set this bit to zero for this iteration
andi x1, x25, 0xf # grab year mod 16
add x1, x1, x23 # add year mod 100
beq x1, x0, LEAP_YEAR # branch if year % 400 == 0 (notice ppcm(100, 16) = 400)
beq x22, x0, YEAR_MOD_4 # branch if year % 4 == 0
beq x0, x0, UPDATE_FEBRUARY # otherwise not a leap year, just branch to update
#
YEAR_MOD_4:
beq x23, x0, UPDATE_FEBRUARY # if year % 4 == 0 and year % 100 == 0, not a leap year
# otherwise, it is a leap year
LEAP_YEAR:
addi x19, x19, 1 # x19 <- 1
#
UPDATE_FEBRUARY:
addi x20, x19, 28 # 28 + whether it is a leap year
bne x27, x20, OUTPUT
xor x27, x27, x27
jal x0, CON
# Deal with other months
OTHER_MONTHS: 
addi x1, x21, 0 # x1 <- x21
srl x1, x1, x26 # get encode bit
andi x1, x1, 1 # corresponding to the month
addi x20, x0, 30 # x20 <- 30
add x2, x1, x20 # x2 <- 30 + encode bit
bne x27, x2, OUTPUT
xor x27, x27, x27

CON:
# increase month
addi x26, x26, 1
addi x20, x0, 12 # x20 <- 12
bne x26, x20, OUTPUT # output and loop
xor x26, x26, x26

# increase year
addi x25, x25, 1
# update year % 400
addi x24, x24, 1
addi x20, x0, 400 # x20 <- 400
bne x24, x20, UPDATE_YEAR100
xor x24, x24, x24
# update year % 100
UPDATE_YEAR100:
addi x23, x23, 1
addi x20, x0, 100 # x20 <- 100
bne x23, x20, UPDATE_YEAR4
xor x23, x23, x23
# update year % 4
UPDATE_YEAR4:
addi x22, x22, 1
addi x20, x0, 4 # x20 <- 4
bne x22, x20, OUTPUT
xor x22, x22, x22
jal x0, OUTPUT

init: # Load all the values, initialise modulos; Loading is done from a string of the form "HH:MM:SS JJ/MM/YYYY"
# at the base of memory space
addi x2, x0, 0 # load hrs
jal x3, readASCII_BCD
addi x28, x1, 0

addi x2, x0, 3 # load mins
jal x3, readASCII_BCD
addi x29, x1, 0

addi x2, x0, 6 # load secs
jal x3, readASCII_BCD
addi x30, x1, 0

addi x2, x0, 9 # load day
jal x3, readASCII_BCD
addi x27, x1, -1

addi x2, x0, 12 # load month
jal x3, readASCII_BCD
addi x26, x1, -1
# Loading year. We setup the modulos at the same time 15 16 17 18

addi x22, x0, 0 # year mod 4   (compute mod 4 of least significant digits)
addi x23, x0, 0 # year mod 100 (load last 2 digits)
addi x25, x0, 0 # year
addi x2, x0, 17
jal x3, readASCII_BCD # Etre divisible par 400 c'est être divisible par 100 = 4*5^2 et 16 = 4^2 !
addi x23, x1, 0
andi x22, x23, 0x3 # keep only 2 LSB
addi x2, x0, 15
jal x3, readASCII_BCD
add x25, x25, x1 # 100 = 2^6 + 2^5 + 2^2 = 2^2(1 + 2^3(1 + 2))
add x25, x25, x1
add x25, x25, x1
slli x25, x25, 3
add x25, x25, x1
slli x25, x25, 2
add x25, x25, x23 # add first two digits

# output to ram and loop
OUTPUT:
addi x1, x0, ':' # lay down :s
sb x1, 2(x0)
sb x1, 5(x0)

addi x1, x30, 0 # print sec
addi x2, x0,  6
jal x3, print_2dg

addi x1, x29, 0 # print min
addi x2, x0,  3
jal x3, print_2dg

addi x1, x28, 0 # print hrs
addi x2, x0,  0
jal x3, print_2dg

addi x1, x0, ' ' # lay down spacing and /
sb x1, 8(x0)
addi x1, x0, '/'
sb x1, 11(x0)
sb x1, 14(x0)

addi x1, x27, 1 # print day, 1-indexed
addi x2, x0, 9
jal x3, print_2dg

addi x1, x26, 1 # print month, 1-indexed
addi x2, x0, 12
jal x3, print_2dg

addi x1, x25, 0 # print year
addi x2, x0, 15
jal x3, print_4dg 

addi x1, x0, 1
csrrw x0, 0, x1 # Set IE = 1
busyloop: jal x0,busyloop

readASCII_BCD: # Loads the BCD 2-digit number from at 0(x2) into x1. Returns through x3
	lb x1, 1(x2)
	andi x1, x1, 0xf # Units digit
	lb x4, 0(x2)
	andi x4, x4, 0xf
	slli x4, x4, 1
	slli x5, x4, 2
	add x4, x4, x5
	add x1, x1, x4
	jalr x0, x3

print_2dg: # Expects value to print in x1, where to print in x2 and returns to x3
	addi x4, x0, '0'
	addi x5, x0, 10
	loop: blt x1, x5, brk
		addi x1, x1, -10
		addi x4, x4,   1
		jal x0, loop
	brk: addi x1, x1, '0' # Now x1 holds the units and x4 the 10s
	sb x4, 0(x2)
	sb x1, 1(x2)
	jalr x0, x3

print_4dg: # Same
	addi x4, x0, 0
	addi x5, x0, 100
	addi x7, x3, 0
	l4: 	blt x1, x5, brk4
		addi x1, x1, -100
		addi x4, x4, 1
		jal x0, l4
	brk4: addi x6, x1, 0
	addi x1, x4, 0 # on écrit les 100aines
	jal  x3, print_2dg
	addi x2, x2, 2 # on incrémente la place
	addi x1, x6, 0 # puis les unités
	jal  x3, print_2dg
	jalr x0, x7
