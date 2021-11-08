#!/bin/sh
(cd kissat; ./configure && make)
(cd cadical; ./configure --competition && make)
(cd drat-trim; make)