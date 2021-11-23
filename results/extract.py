# this script should generate a csv file with the name of each benchmark in every row, and then the following information from the output of the benchmark:
# the following lines have been added to the output
# AUXLIST: %d,%d,%d,%d,%d,%d,%d,%d,%d 
#   * this contains gate types in this order: EQV, DEF, ITE, AND, XOR, FUL, OR, TRI, GEN
# AUX DECISIONS: %d
#   * the number of times auxiliary variables were decided on
# we also want to record the time that "SOLVE" was printed and the time that "VERIFY" was printed; the difference is the duration of the solver actually running.
# we can combine this csv file with results to get our data.