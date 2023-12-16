import sys  
sys.path.append("..")

from lib_carotte import *
import alu.constant as constant

def right_shift_1(a):
    assert(a.bus_size == 32)
    s = constant.z_1 + a[0:31]
    return s

def right_shift_2(a):
    assert(a.bus_size == 32)
    s = constant.z_2 + a[0:30]
    return s

def right_shift_4(a):
    assert(a.bus_size == 32)
    s = constant.z_4 + a[0:28]
    return s

def right_shift_8(a):
    assert(a.bus_size == 32)
    s = constant.z_8 + a[0:24]
    return s

def right_shift_16(a):
    assert(a.bus_size == 32)
    s = constant.z_16 + a[0:16]
    return s

def n_srl(a, b):
    assert(a.bus_size == b.bus_size)
    for i in range(5, b.bus_size):
        a = Mux(b[i], a, constant.z_32)
    a = Mux(b[4], right_shift_16(a), a)
    a = Mux(b[3], right_shift_8(a), a)
    a = Mux(b[2], right_shift_4(a), a)
    a = Mux(b[1], right_shift_2(a), a)
    a = Mux(b[0], right_shift_1(a), a)
    return a
