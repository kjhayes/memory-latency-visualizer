
CC ?= cc
CFLAGS ?=

checkpair: checkpair.c
	$(CC) $(CFLAGS) -pthread $^ -o $@

clean: FORCE
	rm ./checkpair

FORCE:

