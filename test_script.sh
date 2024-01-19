#!/bin/bash
simpath=netlist_sim
for f in $1
do
	echo -e "\033[32m" $f "======================\033[0m"
	lcnt="wc -l ${f%.bin}.s"
	options=""
	if [ -e ${f%.bin}.conf ]
	then
		options=$(cat ${f%.bin}.conf)
	fi
	if [ -e ${f%.bin}.output ]
	then
		$simpath build.net -n$($lcnt) -i/dev/zero -r$f $options | diff -s -w - --label "build output on $f" ${f%.bin}.output
	else
		$simpath build.net -n$($lcnt) -i/dev/zero -r$f $options
	fi
done
