default: clean
	@zip -D -r starexec.zip * -x *.csv -x *.py -x run.sh -x makefile -x README.md

build:
	cd kissat; ./configure && make && cp ./build/kissat ../bin/kissat
	cd cadical; ./configure --competition && make && cp ./build/cadical ../bin/cadical
	cd drat-trim; make && cp drat-trim ../bin/drat-trim
	cd cnftools; mkdir build && cd build && cmake -DCMAKE_BUILD_TYPE=Release .. && make && cp cnftools ../../bin/cnftools

clean:
	@rm -f ./starexec.zip
	@rm -rf ./cadical/build
	@rm -rf ./cnftools/build
	@rm -rf ./kissat/build
	@rm -f ./drat-trim/drat-trim
	@rm -f ./drat-trim/compress
	@rm -f ./drat-trim/decompress
	@rm -f ./drat-trim/lrat-check
	@rm -f ./output
	@rm -f ./bin/kissat
	@rm -f ./bin/cadical
	@rm -f ./bin/cnftools
	@rm -f ./bin/drat-trim