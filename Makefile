
header = src/header
modules = build/module

tests = test/first.log test/nkobject.log 

test:  $(tests)

clean:
	rm test/*; rm build/test/*; rm build/module/*

build/module/first.o: src/module/first.c
	gcc -I$(header) -c src/module/first.c -o build/module/first.o

build/test/first: src/test/first.c src/test/minuint.h build/module/first.o src/header/first.h
	gcc -I$(header) -L$(modules) src/test/first.c -o build/test/first build/module/first.o

test/first.log: build/test/first
	./build/test/first >& test/first.log

build/module/nkobject.o: src/module/nkobject.c
	gcc -I$(header) -c src/module/nkobject.c -o build/module/nkobject.o

build/test/nkobject: src/test/nkobject.c src/test/minuint.h build/module/nkobject.o src/header/nkobject.h
	gcc -I$(header) -L$(modules) src/test/nkobject.c -o build/test/nkobject build/module/nkobject.o

test/nkobject.log: build/test/nkobject
	./build/test/nkobject >& test/nkobject.log

