library(tidyverse)
library(dplyr)
library(openxlsx)
results <- read.csv(file = './results/results.csv') %>% filter(result != "UNKNOWN")
results['percent_variables_auxiliary'] <- results['percent_variables_auxiliary'] * 100
`%notin%` <- Negate(`%in%`)
FILENAME = "./results/better_worse.xlsx"
MARGIN_OF_ERROR_PERCENT = -5
results_all <- results
results <- results %>% group_by(configuration) %>% group_split()
COL_NAMES = c()

for(df in results){
  COL_NAMES <- append(COL_NAMES, df[1,]['configuration'])
}
join_on_attr <- function(dflist, attr, col_names){
    initial <- dflist[[1]] %>% select("benchmark", all_of(attr))
    for(i in 2:length(dflist)){
      temp <- dflist[[i]] %>% select("benchmark", all_of(attr))
      initial <- left_join(initial, temp, by="benchmark")
    }
    colnames(initial) <- col_names
    return(initial)
}

by_mem_usage <- join_on_attr(results, "memory.usage", c("benchmark", COL_NAMES))
by_cpu_usage <- join_on_attr(results, "cpu.time", c("benchmark", COL_NAMES))
by_mem_usage$configuration <- colnames(by_mem_usage)[apply(by_mem_usage[, 2:ncol(by_mem_usage)],1,which.min) + 1]
by_cpu_usage$configuration <- colnames(by_cpu_usage)[apply(by_cpu_usage[, 2:ncol(by_cpu_usage)],1,which.min) + 1]

by_mem_usage$min <- apply(by_mem_usage[, 3:ncol(by_mem_usage)-1], 1, min, na.rm = TRUE)
by_cpu_usage$min <- apply(by_cpu_usage[, 3:ncol(by_cpu_usage)-1], 1, min, na.rm = TRUE)
by_mem_usage$max <- apply(by_mem_usage[, 4:ncol(by_mem_usage)-2], 1, max, na.rm = TRUE)
by_cpu_usage$max <- apply(by_cpu_usage[, 4:ncol(by_cpu_usage)-2], 1, max, na.rm = TRUE)

by_cpu_usage$range <- by_cpu_usage$max - by_cpu_usage$min
by_mem_usage$range <- by_mem_usage$max - by_mem_usage$min

by_mem_usage <- by_mem_usage %>% inner_join(results_all, c("benchmark", "configuration"))
by_cpu_usage <- by_cpu_usage %>% inner_join(results_all, c("benchmark", "configuration"))

better_aux_mem <- by_mem_usage %>% filter(configuration != "control.sh" & configuration != "control_noelim.sh")
better_aux_mem$percent_diff_from_control <- (better_aux_mem$min - better_aux_mem$control.sh) / better_aux_mem$control.sh * 100
better_aux_mem <- as.data.frame(better_aux_mem %>% filter(percent_diff_from_control <= MARGIN_OF_ERROR_PERCENT))

better_aux_cpu <- by_cpu_usage %>% filter(configuration != "control.sh" & configuration != "control_noelim.sh")
better_aux_cpu$percent_diff_from_control <- (better_aux_cpu$min - better_aux_cpu$control.sh) / better_aux_cpu$control.sh * 100
better_aux_cpu <- as.data.frame(better_aux_cpu %>% filter(percent_diff_from_control <= MARGIN_OF_ERROR_PERCENT))

worse_aux_mem <- subset(by_mem_usage, configuration %in% c("control.sh", "control_noelim.sh")  & range >= (MARGIN_OF_ERROR_PERCENT/100)*control.sh)
worse_aux_cpu <- subset(by_cpu_usage, configuration %in% c("control.sh", "control_noelim.sh")  & range >= (MARGIN_OF_ERROR_PERCENT/100)*control.sh)

control_cpu <- results_all %>% filter(configuration == "control.sh") %>% filter(benchmark %in% better_aux_cpu$benchmark)
control_mem <- results_all %>% filter(configuration == "control.sh") %>% filter(benchmark %in% better_aux_mem$benchmark)
runtime_statistic_names <- c("num_decisions", "decisions_per_sec", "num_conflicts", "conflicts_per_sec", "num_restarts", "num_reduced", "percent_reduced_per_conflict", "num_propagations", "propagations_per_sec")

compare_to_control_by_percentage <- function(df, control, col_names){
  subset_df <- select(df, c("benchmark", all_of(runtime_statistic_names)))
  subset_control <- select(control, c("benchmark", all_of(runtime_statistic_names)))

  temp <- merge(subset_df, subset_control, by.x = "benchmark", by.y = "benchmark", all=TRUE)

  for(i in 1:length(col_names)){
    name <- col_names[i]
    diff <- paste(name, ".x", sep="")
    base <- paste(name, ".y", sep="") 
    temp[name] = (temp[diff] - temp[base]) / temp[base] * 100
  }
  temp <- select(temp, c("benchmark", all_of(runtime_statistic_names)))
  colnames(temp) = c("benchmark", lapply(all_of(runtime_statistic_names), paste0, "_percent_diff_from_control"))
  return(temp)
}
better_aux_cpu <- better_aux_cpu %>% inner_join(compare_to_control_by_percentage(better_aux_cpu, control_cpu, runtime_statistic_names), by="benchmark")
better_aux_mem <- better_aux_mem %>% inner_join(compare_to_control_by_percentage(better_aux_mem, control_mem, runtime_statistic_names), by="benchmark")


better_aux_cpu <- better_aux_cpu[,!(names(better_aux_cpu) %in% c("min", "max", "range", COL_NAMES))]
better_aux_mem <- better_aux_mem[,!(names(better_aux_mem) %in% c("min", "max", "range", COL_NAMES))]
worse_aux_mem <- worse_aux_mem[,!(names(worse_aux_mem) %in% c("min", "max", "range", COL_NAMES))]
worse_aux_cpu <- worse_aux_cpu[,!(names(worse_aux_cpu) %in% c("min", "max", "range", COL_NAMES))]

wb <- createWorkbook()
addWorksheet(wb, "Solved faster than control")
writeDataTable(wb, 1, better_aux_cpu)

addWorksheet(wb, "Used less memory than control")
writeDataTable(wb, 2, better_aux_mem)

addWorksheet(wb, "Solved faster with less memory")
writeDataTable(wb, 3, inner_join(better_aux_cpu, better_aux_mem))

addWorksheet(wb, "Solved slower than control")
writeDataTable(wb, 4, worse_aux_cpu)

addWorksheet(wb, "Used more memory than control")
writeDataTable(wb, 5, worse_aux_mem)

saveWorkbook(wb, FILENAME, overwrite = TRUE)