#!/bin/sh
(cd kissat; ./configure && make && cp ./build/kissat ../bin/kissat)
(cd cadical; ./configure --competition && make && cp ./build/cadical ../bin/cadical)
(cd drabt; ./configure.sh && make && cp drabt ../bin/drabt)