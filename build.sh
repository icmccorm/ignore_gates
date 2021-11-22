#!/bin/sh
(cd kissat; ./configure && make && cp ./build/kissat ../bin/kissat)
(cd cadical; ./configure && make && cp ./build/cadical ../bin/cadical)
(cd drabt; ./configure.sh && make && cp drabt ../bin/drabt)
(cp ./kissat/select_aux.py ./bin/select_aux.py)