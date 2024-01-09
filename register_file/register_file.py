from lib_carotte import *
from utils import *

NUM_REGISTER = 32
SIZE_REGISTER = 32

def register_file():
    # input
    oa1 = Input(5)
    oa2 = Input(5)
    ia1 = Input(5)
    data_in = Input(32)
    pc_in = Input(32)

    # registers
    def get_register(i, j):
        return lambda: reg[i][j]
    pre_reg = [None] + [[Reg(Defer(1, get_register(i, j))) for j in range(SIZE_REGISTER)] for i in range(1, NUM_REGISTER)]
    reg = [[Select(i, pc_in) for i in range(SIZE_REGISTER)]]
    update = demux1to32(Constant("1"), ia1)
    # update the registers
    for i in range(1, NUM_REGISTER):
        reg.append(b32mux2to1(pre_reg[i], data_in, update[i]))
        # temp = union(b32mux2to1(pre_reg[i], data_in, update[i]))
        # temp.set_as_output("reg" + str(i))
        # temp2 = union(pre_reg[i])
        # temp2.set_as_output("pre_reg" + str(i))
    # compute the output
    pc_out = union(reg[0])
    zero32 = [Constant("0")] * 32
    out1 = union(b32mux32to1([zero32]+reg[1:], oa1))
    out2 = union(b32mux32to1([zero32]+reg[1:], oa2))

    # output
    pc_out.set_as_output("pc_out")
    out1.set_as_output("out1")
    out2.set_as_output("out2")

def main():
    register_file()