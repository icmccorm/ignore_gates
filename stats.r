library(purrr)
library(ggplot2)
library(tidyverse)
library(dplyr)
library(xlsx)
kissat <- read.csv(file = './results/kissat/info.csv') %>% filter(result != "UNKNOWN")
cnftools <- read.csv(file = './results/cnftools/info.csv') %>% filter(result != "UNKNOWN")
control <- read.csv(file = './results/control/info.csv') %>% filter(result != "UNKNOWN")
kissat_elimaux <- read.csv(file = './results/kissat-elimaux/info.csv') %>% filter(result != "UNKNOWN")
cnftools_elimaux <- read.csv(file = './results/cnftools-elimaux/info.csv') %>% filter(result != "UNKNOWN")
x_axis <- seq(0, 5000, 1)

DATA_SETS <- list(kissat, cnftools, kissat_elimaux, cnftools_elimaux, control)
COL_NAMES <- c("kissat", "cnftools", "kissat_elimaux", "cnftools_elimaux", "control")
MARGIN_OF_ERROR_PERCENT = 5
FILENAME = "./results/results.xlsx"

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
            DATA_SETS
        )
)))
colnames(all) <- c("time", "kissat", "cnftools", "kissat_elimaux", "cnftools_elimaux", "control")

all <- all %>%
  select(time, kissat, cnftools, kissat_elimaux, cnftools_elimaux, control) %>%
  gather(key = "variable", value = "value", -time)

ggplot(all, aes(x = value, y = time)) + 
  geom_line(aes(color = variable)) +
  ggtitle("Results from branching only on problem variables") +
  ylab("CPU Time (in seconds)") +
  xlab("Number of problems solved") 

join_on_attr <- function(dflist, attr, col_names){
    initial <- dflist[[1]] %>% select("benchmark", attr)
    for(i in 2:length(dflist)){
      temp <- dflist[[i]] %>% select("benchmark", attr)
      initial <- left_join(initial, temp, by="benchmark")
    }
    colnames(initial) <- col_names
    return(initial)
}
by_mem_usage <- join_on_attr(DATA_SETS, "memory.usage", c("benchmark", COL_NAMES))
by_cpu_usage <- join_on_attr(DATA_SETS, "cpu.time", c("benchmark", COL_NAMES))


by_mem_usage$min <- apply(by_mem_usage[, 2:ncol(by_mem_usage)], 1, min)
by_cpu_usage$min <- apply(by_cpu_usage[, 2:ncol(by_cpu_usage)], 1, min)
by_mem_usage$max <- apply(by_mem_usage[, 2:ncol(by_mem_usage)], 1, max)
by_cpu_usage$max <- apply(by_cpu_usage[, 2:ncol(by_cpu_usage)], 1, max)

by_cpu_usage$range <- by_cpu_usage$max - by_cpu_usage$min
by_mem_usage$range <- by_mem_usage$max - by_mem_usage$min

better_aux_mem <- subset(by_mem_usage, max == control & range >= (MARGIN_OF_ERROR_PERCENT/100)*control)
better_aux_mem$diff_from_control <- better_aux_mem$range / better_aux_mem$control * 100

better_aux_cpu <- subset(by_cpu_usage, max == control & range >= (MARGIN_OF_ERROR_PERCENT/100)*control)
better_aux_cpu$diff_from_control <- better_aux_cpu$range / better_aux_cpu$control * 100

worse_aux_mem <- subset(by_mem_usage, min == control & range >= (MARGIN_OF_ERROR_PERCENT/100)*control)
worse_aux_cpu <- subset(by_cpu_usage, min == control & range >= (MARGIN_OF_ERROR_PERCENT/100)*control)


write.xlsx(by_cpu_usage,FILENAME, sheetName="All CPU Time", row.names = FALSE)
write.xlsx(by_mem_usage,FILENAME, sheetName="All Memory Usage", row.names = FALSE, append = TRUE)
write.xlsx(better_aux_mem, FILENAME, row.names = FALSE, append = TRUE, sheetName="Better Memory Usage")
write.xlsx(better_aux_cpu, FILENAME, row.names = FALSE, append = TRUE, sheetName="Better CPU Time")
write.xlsx(worse_aux_mem, FILENAME, row.names = FALSE, append = TRUE, sheetName="Worse Memory Usage")
write.xlsx(worse_aux_cpu, FILENAME, row.names = FALSE, append = TRUE, sheetName="Worse CPU Time")
