car=../carotte.py/carotte.py
modules=decoder/*.py ram_interface/*.py register_file/*.py alu/*.py interrupts/*.py
tests= $(wildcard tests/*.s)

.PHONY: project clean test
project: build.net test

test: $(tests:.s=.bin) | build.net
	./test_script.sh "$^"
%.bin: %.s
	./assemble_script.sh $< $@

build.net: cpu.py $(modules)
	 $(car) cpu.py > build.net
clean:
	rm build.net $(tests:.s=.bin) &> /dev/null
