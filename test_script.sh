#!/bin/sh
lcnt="wc -l ${1%.bin}.s"
simpath=netlist_sim
$simpath build.net -n$($lcnt) -r$1
