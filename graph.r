library(purrr)
library(ggplot2)
library(tidyverse)
library(dplyr)
kissat <- read.csv(file = './results/kissat/info.csv') %>% filter(result != "UNKNOWN")
cnftools <- read.csv(file = './results/cnftools/info.csv') %>% filter(result != "UNKNOWN")
control <- read.csv(file = './results/control/info.csv') %>% filter(result != "UNKNOWN")
kissat_elimaux <- read.csv(file = './results/kissat-elimaux/info.csv') %>% filter(result != "UNKNOWN")
cnftools_elimaux <- read.csv(file = './results/cnftools-elimaux/info.csv') %>% filter(result != "UNKNOWN")
x_axis <- seq(0, 5000, 1)



num_completed <- function(time, dflist) {
    result = c(time)
    for(i in 1:length(dflist)){
        curr_df <- dflist[[i]]
        less <- curr_df[curr_df['cpu.time'] < time,]
        result <- append(result, c(nrow(less)))
    }
    return(result)
}
all <- as.data.frame(do.call(rbind, map(
        x_axis, 
        ~ num_completed(
            .x, 
            list(kissat, cnftools, control, kissat_elimaux, cnftools_elimaux)
        )
)))
colnames(all) <- c("time", "kissat", "cnftools", "control", "kissat_elimaux", "cnftools_elimaux")

all <- all %>%
  select(time, kissat, cnftools, control, kissat_elimaux, cnftools_elimaux) %>%
  gather(key = "variable", value = "value", -time)

ggplot(all, aes(x = value, y = time)) + 
  geom_line(aes(color = variable)) +
  ggtitle("Results from branching only on problem variables") +
  ylab("CPU Time (in seconds)") +
  xlab("Number of problems solved") 