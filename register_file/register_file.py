import sys
sys.path.append("/home/salsifi/cours/di_sysnum/carotte.py")
from lib_carotte import *
from register_file.utils import *

NUM_REGISTER = 32
SIZE_REGISTER = 32

def register_file(oa1, oa2, ia1, data_in, pc_in, x0_in, pc_override, pc_alu, save_pc, eqsel):
    ONE32 = Constant("11111111111111111111111111111111")
    ZERO32 = Constant("00000000000000000000000000000000")
    # input
    assert(oa1.bus_size == 5)
    assert(oa2.bus_size == 5)
    assert(ia1.bus_size == 5)
    #assert(data_in.bus_size == 32) # data_in is treated like a 32-bit wide list of bits (!)
    assert(pc_in.bus_size == 32)
    assert(x0_in.bus_size == 32)
    assert(pc_override.bus_size == 1)
    assert(pc_alu.bus_size == 1)
    assert(save_pc.bus_size == 1)
    assert(eqsel.bus_size == 1)

    # registers
    pc = mux2to1(pc_in, data_in, pc_override)
    reg = [Reg(Defer(32, lambda: pc))]
    update = demux1to32(Constant("1"), ia1)
    # update the registers
    update_ia1 = mux2to1(data_in, x0_in, save_pc) # choose data_in or x0 depending on save_pc
    def get_pre_register(i):
        return lambda: mux2to1(reg[i], update_ia1, Select(i, update))
    for i in range(1, NUM_REGISTER):
        reg.append(Reg(Defer(32, get_pre_register(i))))
    # compute the output
    r_oa1 = mux32to1([ZERO32]+reg[1:], oa1)
    r_oa2 = mux32to1([ZERO32]+reg[1:], oa2)
    lt, temp_eq = cmp(r_oa1, r_oa2)
    eq = ((~eqsel) & temp_eq) | (eqsel & (lt | temp_eq))
    out1 = r_oa1
    out2 = mux2to1(r_oa2, reg[0], pc_alu)

    # output
    #reg[0].set_as_output("pc_out")
    #out1.set_as_output("out1")
    #out2.set_as_output("out2")
    #eq.setas_output("eq")
    return (out1, out2, reg[0], eq)

def test():
    # allow_ribbon_logic_operations(True)
    oa1 = Input(5)
    oa2 = Input(5)
    ia1 = Input(5) 
    data_in = Input(32)
    pc_in = Input(32)
    x0_in = Input(32)
    pc_override = Input(1)
    pc_alu = Input(1)
    save_pc = Input(1)
    eqsel = Input(1)
    out1, out2, pc_out, eq = register_file(oa1, oa2, ia1, data_in, pc_in, x0_in,
                                           pc_override, pc_alu, save_pc, eqsel)
    out1.set_as_output("out1")
    out2.set_as_output("out2")
    pc_out.set_as_output("pc_out")
    eq.set_as_output("eq")