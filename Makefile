
.PHONY: clean test

CC = clang
SUFFIXES = .test .o .c .h .log

header_path = src/header
src_path = src/module
module_path = build/module
test_path = build/test

MODULES = first.o knobject.o kngc.o knstring.o
SRC = $(MODULES:%.o=%.c)
HDR = $(MODULES:%.o=%.h)
TEST = $(MODULES:%.o=%.test)
LOG = $(MODULES:%.o=%.log)


vpath %.log test
vpath %.o build/module
vpath %.c src/module src/test
vpath %.test build/test
vpath %.h src/header


test:  $(LOG)

clean: clean_log clean_test clean_obj

clean_log:
	-$(RM) test/*.log;

clean_test:
	-$(RM) build/test/*.test;

clean_mod:
	-$(RM) build/module/*.o


$(MODULES): $(@:.o=%.c) $(@:%.o=%.h)
	gcc -I$(header_path) -c $(src_path)/$< -o $(module_path)/$@

.test.o:
	gcc -I$(header_path) -L$(module_path) -o $(test_path)/$@ src/test/$< build/module/*.o


$(LOG): $(@:.log=%.test)
	./build/test/$< >& test/$@

build/module/peer.o: src/module/peer.c src/header/peer.h
	gcc -I$(header_path) -c src/module/peer.c -o build/module/peer.o


