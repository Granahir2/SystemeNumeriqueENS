car=../carotte.py/carotte.py
modules=decoder/*.py ram_interface/*.py register_file/*.py alu/*.py interrupts/*.py
tests= $(wildcard tests/*.s)

.PHONY: project clean test clock
project: build.net test clock

test: $(tests:.s=.bin) | build.net
	./test_script.sh "$^"
clock: clock/clock.bin
	
%.bin: %.s
	./assemble_script.sh $< $@

build.net: cpu.py $(modules)
	 $(car) cpu.py > build.net
clean:
	rm build.net $(tests:.s=.bin) clock/clock.bin
