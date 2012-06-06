
header = src/header
modules = build/module

tests = test/first.log test/knobject.log 

test:  $(tests)

clean:
	rm test/*; rm build/test/*; rm build/module/*

build/module/first.o: src/module/first.c
	gcc -I$(header) -c src/module/first.c -o build/module/first.o

build/test/first: src/test/first.c src/test/minuint.h build/module/first.o src/header/first.h
	gcc -I$(header) -L$(modules) src/test/first.c -o build/test/first build/module/first.o

test/first.log: build/test/first
	./build/test/first >& test/first.log

build/module/knobject.o: src/module/knobject.c
	gcc -I$(header) -c src/module/knobject.c -o build/module/knobject.o

build/test/knobject: src/test/knobject.c src/test/minuint.h build/module/knobject.o src/header/knobject.h
	gcc -I$(header) -L$(modules) src/test/knobject.c -o build/test/knobject build/module/knobject.o

test/knobject.log: build/test/knobject
	./build/test/knobject >& test/knobject.log

