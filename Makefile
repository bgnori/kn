
header = src/header
modules = build/module

test:  test/first.log

clean:
	rm test/*; rm build/test/*; rm build/module/*

build/module/first.o: src/module/first.c
	gcc -I$(header) -c src/module/first.c -o build/module/first.o

build/test/first: src/test/first.c src/test/minuint.h build/module/first.o src/header/first.h
	gcc -I$(header) -L$(modules) src/test/first.c -o build/test/first build/module/first.o

test/first.log: build/test/first
	./build/test/first >& test/first.log

