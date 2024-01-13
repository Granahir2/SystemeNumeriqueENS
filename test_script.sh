#!/bin/sh
simpath=netlist_sim
for f in $1
do
	echo "\033[32m" $f "======================\033[0m"
	lcnt="wc -l ${f%.bin}.s"
	$simpath build.net -n$($lcnt) -r$f
done
