#!/bin/bash
simpath=netlist_sim
$simpath ../build.net -rclock.bin -q -w19 -g"""$(date +"%H:%M:%S %d/%m/%Y")""" -cIRQ -i/dev/zero "$1" "$2"
