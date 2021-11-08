#!/bin/sh
(cd kissat; ./configure && make && cp ./build/kissat ../bin/kissat)
(cd cadical; ./configure --competition && make && cp ./build/cadical ../bin/cadical)
(cd drat-trim; make && cp drat-trim ../bin/drat-trim)
(cd cnftools; mkdir build && cd build && cmake -DCMAKE_BUILD_TYPE=Release .. && make && cp cnftools ../../bin/cnftools)
