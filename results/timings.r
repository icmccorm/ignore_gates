library(tidyverse)
library(dplyr)
library(openxlsx)
x_axis <- seq(0, 5000, 1)
results <- read.csv(file = './results/results.csv') %>% filter(result != "UNKNOWN")
`%notin%` <- Negate(`%in%`)

num_completed <- function(time, dflist) {
    result = c(time)
    for(i in 1:length(dflist)){
        curr_df <- dflist[[i]]
        less <- curr_df[curr_df['cpu.time'] < time,]
        result <- append(result, c(nrow(less)))
    }
    return(result)
}

all_sat <- results %>% filter(result == "SAT-INCORRECT")
all_unsat <- results %>% filter(result == "UNSAT")

sat_grouped <- all_sat %>% filter(NUM_AUX > 0 | configuration %in% c("control", "control.noelim", "control.sideeffects", "control.lastuip")) %>% group_by(configuration) %>% group_split()
unsat_grouped <- all_unsat %>% filter(NUM_AUX > 0 | configuration %in% c("control", "control.noelim", "control.sideeffects", "control.lastuip")) %>% group_by(configuration) %>% group_split()
col_names_sat = c("time")
for(df in sat_grouped){
  col_names_sat <- append(col_names_sat, df[1,]['configuration'])
}
col_names_unsat = c("time")
for(df in unsat_grouped){
  col_names_unsat <- append(col_names_unsat, df[1,]['configuration'])
}
sat_timed <- as.data.frame(do.call(rbind, map(
        x_axis, 
        ~ num_completed(
            .x, 
            sat_grouped
        )
)))
colnames(sat_timed) = col_names_sat
unsat_timed <- as.data.frame(do.call(rbind, map(
        x_axis, 
        ~ num_completed(
            .x, 
            unsat_grouped
        )
)))
colnames(unsat_timed) = col_names_unsat

write.csv(sat_timed, file = './results/sat_timed.csv')
write.csv(unsat_timed, file = './results/unsat_timed.csv')
