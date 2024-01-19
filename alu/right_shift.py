import sys  
sys.path.append("..")

from lib_carotte import *
import alu.constant as constant

def right_shift_1(a):
    assert(a.bus_size == 32)
    s = a[1:32] + constant.z_1
    return s

def right_shift_2(a):
    assert(a.bus_size == 32)
    s = a[2:32] + constant.z_2
    return s

def right_shift_4(a):
    assert(a.bus_size == 32)
    s = a[4:32] + constant.z_4
    return s

def right_shift_8(a):
    assert(a.bus_size == 32)
    s = a[8:32] + constant.z_8
    return s

def right_shift_16(a):
    assert(a.bus_size == 32)
    s = a[16:32] + constant.z_16
    return s

def n_srl(a, b):
    assert(a.bus_size == b.bus_size)

    def or_accumulator(a):
        sz = a.bus_size
        if sz == 1:
            return a[0]
        else:
            return or_accumulator(a[sz//2-1]) | or_accumulator(a[sz//2:])

    a = Mux(b[4], a, right_shift_16(a))#, a)
    a = Mux(b[3], a, right_shift_8(a))#, a)
    a = Mux(b[2], a, right_shift_4(a))#, a)
    a = Mux(b[1], a, right_shift_2(a))#, a)
    a = Mux(b[0], a, right_shift_1(a))#, a)
    #a = Mux(or_accumulator(Constant("00000") + b), a, constant.z_32)
            
    return (a, ~or_accumulator(a))
