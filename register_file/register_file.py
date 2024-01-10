from lib_carotte import *
from utils import *

NUM_REGISTER = 32
SIZE_REGISTER = 32

def register_file():
    ONE32 = Constant("11111111111111111111111111111111")
    ZERO32 = Constant("00000000000000000000000000000000")
    # input
    oa1 = Input(5)
    oa2 = Input(5)
    ia1 = Input(5)
    data_in = Input(32)
    pc_in = Input(32)

    # registers
    dummy_pc_in = pc_in & ONE32
    reg = [Reg(Defer(32, lambda: dummy_pc_in))]
    update = demux1to32(Constant("1"), ia1)
    # update the registers
    def get_pre_register(i):
        return lambda: mux2to1(reg[i], data_in, Select(i, update))
    for i in range(1, NUM_REGISTER):
        reg.append(Reg(Defer(32, get_pre_register(i))))
    # compute the output
    out1 = mux32to1([ZERO32]+reg[1:], oa1)
    out2 = mux32to1([ZERO32]+reg[1:], oa2)

    # output
    reg[0].set_as_output("pc_out")
    out1.set_as_output("out1")
    out2.set_as_output("out2")

def main():
    allow_ribbon_logic_operations(True)
    register_file()