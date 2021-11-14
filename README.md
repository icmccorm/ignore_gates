# 15-816 Final Project: Ignoring Gate Literals

## Testing & Uploading

To package everything for upload to starexec, run `make`. 

To build the solver locally, execute `make build` in the root directory. This will create binaries for each solver/tool in `./bin`.

To run the solver, execute `run.sh [name of cnf file]` in the root directory.

## Viewing Results

Run the unmodified cadical and this configuration on the 400 benchmarks from the 2021 SAT Competition. Download the job info `.csv` files from each. Name the results from CaDiCaL-sc2021 `original.csv`, name the results from this configuration `nogates.csv`, and place both in the root directory. Then, execute `python ./plot.py`. This requires the libraries `matplotlib`, `numpy`, and `pandas`.

## Verifying Results
To verify SAT and UNSAT results from running our tool, download the job output from StarExec. This will provide a directory with the following structure:

```
Job_output
    |_[space name]
        |_[job name]
            |_benchmark1
            |_benchmark2
            |_...
```

Copy the `[job name]` folder into the root directory of the repository and rename it `output`. Then, execute `verify.py`.