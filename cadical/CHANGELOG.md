
# parse.cpp
- Added `Parser::parse_aux` method for reading in a list of auxiliary variables. 

# external.hpp/external.cpp
- Added `std::unordered_map<int, bool> aux` to contain the list of auxiliary variables. 
    * Replace with hashset
- Added `External::add_aux` to add an auxiliary variable to the map.
- Added `External::is_aux` which returns true if a given external literal is auxiliary.

# cadical.cpp
- Added `-a` option to take in a list of auxiliary variables and their gate types.
- Removed option for piping in `.cnf` files.
- Added option for piping in a list of auxiliary variables if `-a` is not provided.

# queue.cpp
- In `Internal::init_queue`, check if a literal is auxiliary before adding it to the queue

# backtrack.cpp
- In `Internal::unassign`, only push an unassigned variable back on the scores heap or decision queue if it isn't auxiliary. 

# score.cpp
- In `Internal::init_scores`, check if a literal is auxiliary before adding it to the heap
- In `Internal::shuffle_scores`, if `opts.shufflerandom` is enabled, ensure that only problem variables are re-added for shuffling and offset `max_var` accordingly.
