# gates.cpp
- In `kissat_find_gates`, when a gate literal is identified, the external literal and a three-character gate type identifier are printed out. Gate type identifiers include: EQV, AND, ITE, XOR, DEF. The expression `abs(kissat_export_literal(solver, lit))` is used to produce the external representation of an internal literal.

# resolve.c
- In `occurrences_literal`, the call to `kissat_eliminate_binary` is commented out
- In `generate_resolvents`, all calls to `kissat_eliminate_clause` are commented out
- `kissat_generate_resolvents`
    * the check against `occlim` is commented out
    * the function will no longer before finding gates if a literal is pure.

# eliminate.c
- In `set_next_elimination_bound`, the call to `try_to_eliminate_all_variables_again` is commented out
- In `eliminate_variable`, all code except for the call to `kissat_generate_resolvents` is commented out

# search.c
- In `kissat_search`, `kissat_eliminate` is called and then the function exits.

Across many files, default logging has been removed.