# 15-816 Final Project: Ignoring Gate Literals

## Testing & Uploading

To package everything for upload to starexec, run `make`. 

To build the solver locally, execute `make build` in the root directory. This will create binaries for each solver/tool in `./bin`.

To run the solver, execute `run.sh [name of cnf file]` in the root directory.

## Viewing Results

Run the unmodified cadical and this configuration on the 400 benchmarks from the 2021 SAT Competition. Download the job info `.csv` files from each. Name the results from CaDiCaL-sc2021 `original.csv`, name the results from this configuration `nogates.csv`, and place both in the root directory. Then, execute `python ./plot.py`. This requires the libraries `matplotlib`, `numpy`, and `pandas`.