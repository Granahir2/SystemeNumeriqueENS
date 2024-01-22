# A minimal RISCV CPU with interrupts
The repository contains what's needed to compile a CPU to a netlist and run it. It also contains a clock as a sample program.
The repository uses netlist simulator [netlist\_sim] . While in theory it can run on all netlist simulators the bash scripts
may have to be updated.

The CPU is a RISCV rv32i compliant core with a few exceptions :
- all load instructions are signed
- comparisons on branches are always unsigned
- right shifts are always logical
- `SLT(U)` instructions are not supported
- opcode `SYSTEM` only supports instructions `CSRRW`, used to access 3 CSRs : `IE` (CSR 0), `IF` (CSR 1), `IRA` (CSR 2).

These are used to support interrupts according to the following logic : if, during a cycle, the IRQ input is
1 then `IE` becomes `0x01` next cycle. At any given time if both `IE[0]` and `IF[0]` are 1 then the current instruction
is not executed, the current value of `PC` is saved inside `IRA` and in the next cycle `PC` gets value 4.

We use binutils with target platform riscv64-unknown-elf to assemble the test programs as well as the clock.
Testing is run each build by the Makefile.
