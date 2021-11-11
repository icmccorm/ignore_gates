default: clean
	@zip -D -r starexec.zip * -x *.csv -x *.py -x run.sh -x makefile -x README.md -x output/* -x *.cnf

build: clean
	cd kissat; ./configure && make && cp ./build/kissat ../bin/kissat
	cd cadical; ./configure --competition && make && cp ./build/cadical ../bin/cadical
	cd drat-trim; make && cp drat-trim ../bin/drat-trim

clean:
	@rm -f ./starexec.zip
	@rm -rf ./cadical/build
	@rm -rf ./kissat/build
	@rm -f ./drat-trim/drat-trim
	@rm -f ./drat-trim/compress
	@rm -f ./drat-trim/decompress
	@rm -f ./drat-trim/lrat-check
	@rm -f ./bin/kissat
	@rm -f ./bin/cadical
	@rm -f ./cnftools/build
	@rm -f ./bin/drat-trim