from lib_carotte import *

def demux1to4(d, s):
    assert(s.bus_size == 2)
    s0 = Select(0, s)
    s1 = Select(1, s)
    y0 = (~s0) & (~s1) & d
    y1 = s0 & (~s1) & d
    y2 = (~s0) & s1 & d
    y3 = s0 & s1 & d
    return y0 + y1 + y2 + y3

def demux1to8(d, s):
    assert(s.bus_size == 3)
    return demux1to4(~Select(2, s) & d, Slice(0, 2, s)) + demux1to4(Select(2, s) & d, Slice(0, 2, s))

def demux1to32(d, s):
    assert(s.bus_size == 5)
    y = demux1to4(d, Slice(3, 5, s))
    res = demux1to8(y[0], Slice(0, 3, s))
    for i in range(1, len(y)):
        res = res + demux1to8(y[i], Slice(0, 3, s))
    return res

def dup32(b):
    for i in range(5):
        b += b
    return b

def mux2to1(d0, d1, s):
    return (And(d0,(~dup32(s))))|(And(d1,dup32(s)))

def mux4to1(d, s):
    return mux2to1(mux2to1(d[0], d[1], Select(0, s)), mux2to1(d[2], d[3], Select(0, s)), Select(1, s))

def mux8to1(d, s):
    return mux2to1(mux4to1(d[0:4], Slice(0, 2, s)), mux4to1(d[4:8], Slice(0, 2, s)), Select(2, s))

def mux32to1(d, s):
    return mux4to1([mux8to1(d[i:i+8], Slice(0, 3, s)) for i in range(0, 32, 8)], Slice(3, 5, s))

# def b32mux2to1(d0, d1, s):
#     return [mux2to1(d0[i], d1[i], s) for i in range(32)]

# def b32mux32to1(d, s):
#     return [mux32to1([d[i][j] for i in range(32)], s) for j in range(32)]

# def union(l):
#     res = l[0]
#     for i in range(1, len(l)):
#         res = res + l[i]
#     return res
