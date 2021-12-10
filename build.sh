#!/bin/sh
#(cd kissat; ./configure && make && cp ./build/kissat ../bin/kissat)
(cd cadical; ./configure && make && cp ./build/cadical ../bin/control)
(cd drat-trim; make && cp drat-trim ../bin/drat-trim)
#(cp ./kissat/select_aux.py ./bin/select_aux.py)
#(cd cadical; ./configure CXXFLAGS="-DELIMAUX" && make && cp ./build/cadical ../bin/elim)
#(cd cadical; ./configure CXXFLAGS="-DBRANCHAUX" && make && cp ./build/cadical ../bin/br-elim)
#(cd cadical; ./configure CXXFLAGS="-DELIMAUX -DUIPAUX -DBRANCHAUX" && make && cp ./build/cadical ../bin/br-elim-uip)