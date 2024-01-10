import sys
sys.path.append("/home/salsifi/cours/di_sysnum/carotte.py")
from lib_carotte import *
from register_file.utils import *

NUM_REGISTER = 32
SIZE_REGISTER = 32

def register_file(oa1, oa2, ia1, data_in, pc_in):
    ONE32 = Constant("11111111111111111111111111111111")
    ZERO32 = Constant("00000000000000000000000000000000")
    # input
    assert(oa1.bus_size == 5)
    assert(oa2.bus_size == 5)
    assert(ia1.bus_size == 5)
    #assert(data_in.bus_size == 32) # data_in is treated like a 32-bit wide list of bits (!)
    assert(pc_in.bus_size == 32)

    # registers
    dummy_pc_in = pc_in #& ONE32
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
    #reg[0].set_as_output("pc_out")
    #out1.set_as_output("out1")
    #out2.set_as_output("out2")
    return (out1, out2, reg[0])

def test():
	oa1 = Input(5)
	oa2 = Input(5)
	ia1 = Input(5)
	data_in = Input(32)
	pc_in = Input(32)

