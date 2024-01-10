from lib_carotte import *

word_size = 32

def ram_interface(DATA_IN_RAM, DATA_IN_CPU, WIDTH):
    empty_word = Constant("0"*word_size) # do sign extension ?
        
    DATA_OUT_CPU = Mux(
                Select(0, WIDTH),

                Mux(
                    Select(1, WIDTH),
                    Concat(Slice(0, 8, DATA_IN_RAM), Slice(8, word_size, empty_word)),
                    DATA_IN_RAM
                ),

                Concat( Slice(0, 16, DATA_IN_RAM), Slice(16, word_size, empty_word) )
            )

    DATA_OUT_RAM = Mux(
                Select(0, WIDTH),

                Mux(
                    Select(1, WIDTH),
                    Concat(Slice(0, 8, DATA_IN_CPU), Slice(8, word_size, DATA_IN_RAM)),
                    DATA_IN_CPU
                ),

                Concat( Slice(0, 16, DATA_IN_CPU), Slice(16, word_size, DATA_IN_RAM) )
            )

    return (DATA_OUT_CPU, DATA_OUT_RAM)

