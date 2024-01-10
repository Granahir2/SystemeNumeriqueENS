car=../carotte.py/carotte.py
modules=decoder/*.py ram_interface/*.py register_file/*.py alu/*.py
tests=tests/test.bin

.PHONY: project clean
project: build.net test

test: $(tests)
	./test_script.sh $<
%.bin: %.s
	./assemble_script.sh $< $@

build.net: cpu.py
	$(car) cpu.py > build.net
cpu.py:	modules
	
modules:
	
clean:
	rm build.net $(tests) > /dev/null
