#!/bin/bash
TMP=_$1.o
riscv64-unknown-elf-as $1 -march=rv32i -o TMP && riscv64-unknown-elf-objcopy -O binary -j .text TMP $2
rm TMP
