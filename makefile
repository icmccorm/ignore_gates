default: clean
	@zip -D -r starexec.zip * -x '*/.git/*' -x 'cnf/*' -x 'output/*' -x *.csv -x *.py -x run.sh -x makefile -x README.md -x output/* -x *.cnf

build: clean
	cd kissat; ./configure && make && cp ./build/kissat ../bin/kissat
	cd cadical; ./configure --competition && make && cp ./build/cadical ../bin/cadical
	cd drabt; ./configure.sh && make && cp drabt ../bin/drabt

clean: clean-cnf
	@rm -f ./starexec.zip
	@rm -rf ./cadical/build
	@rm -rf ./kissat/build
	@rm -f ./drabt/drabt
	@rm -f ./bin/kissat
	@rm -f ./bin/cadical
	@rm -f ./bin/drabt

clean-cnf:
	@rm -rf ./cnftools/build



cnftools: clean-cnf
	@rm -rf ./cnftools/build; mkdir ./cnftools/build && cd ./cnftools/build && cmake -DCMAKE_BUILD_TYPE=Release .. && make

