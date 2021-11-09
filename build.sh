#!/bin/sh
(cd kissat; ./configure && make && cp ./build/kissat ../bin/kissat)
(cd cadical; ./configure --competition && make && cp ./build/cadical ../bin/cadical)
(cd drat-trim; make && cp drat-trim ../bin/drat-trim)