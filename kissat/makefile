all:
	$(MAKE) -C "/Users/icmccorm/git/kissat/build"
kissat:
	$(MAKE) -C "/Users/icmccorm/git/kissat/build" kissat
tissat:
	$(MAKE) -C "/Users/icmccorm/git/kissat/build" tissat
clean:
	rm -f "/Users/icmccorm/git/kissat"/makefile
	-$(MAKE) -C "/Users/icmccorm/git/kissat/build" clean
	rm -rf "/Users/icmccorm/git/kissat/build"
coverage:
	$(MAKE) -C "/Users/icmccorm/git/kissat/build" coverage
indent:
	$(MAKE) -C "/Users/icmccorm/git/kissat/build" indent
test:
	$(MAKE) -C "/Users/icmccorm/git/kissat/build" test
.PHONY: all clean coverage indent kissat test tissat
