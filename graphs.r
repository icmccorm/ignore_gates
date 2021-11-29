library(ggplot2)
library(tidyverse)
library(dplyr)
library(openxlsx)
library(RColorBrewer)
PALETTE = c("#A6CEE3", "#1F78B4", "#B2DF8A", "#33A02C", "#FB9A99", "#E31A1C", "#FDBF6F", "#FF7F00", "#CAB2D6", "#6A3D9A", "#FFFF99", "#B15928")


sat_timings <- read.csv(file = './results/sat_timed.csv')
unsat_timings <- read.csv(file = './results/unsat_timed.csv')
sat_timings <- sat_timings[,!(names(sat_timings) %in% c("X"))]
unsat_timings <- unsat_timings[,!(names(unsat_timings) %in% c("X"))]

sat_timings_kissat <- select(sat_timings, !contains("cnftools")) %>% gather(key = "variable", value = "value", -time)
sat_timings_cnftools <- select(sat_timings, !contains("kissat")) %>% gather(key = "variable", value = "value", -time)

unsat_timings_kissat <- select(unsat_timings, !contains("cnftools")) %>% gather(key = "variable", value = "value", -time)
unsat_timings_cnftools <- select(unsat_timings, !contains("kissat")) %>% gather(key = "variable", value = "value", -time)

sat_timings <- sat_timings %>% gather(key = "variable", value = "value", -time)
unsat_timings <- unsat_timings %>% gather(key = "variable", value = "value", -time)

ggplot(sat_timings, aes(x = time, y = value, color = variable)) + 
  geom_line() +
  scale_color_manual(values=c("#A6CEE3", "#1F78B4", "#B2DF8A", "#33A02C", "#FB9A99", "#E31A1C", "#FDBF6F", "#FF7F00", "#CAB2D6", "#6A3D9A", "#FFFF99", "#B15928")) +
  ggtitle("All SAT results") +
  xlab("CPU Time (in seconds)") +
  ylab("Number of problems solved") 

ggplot(unsat_timings, aes(x = time, y = value, color=variable)) + 
  geom_line() +
  scale_color_manual(values=c("#A6CEE3", "#1F78B4", "#B2DF8A", "#33A02C", "#FB9A99", "#E31A1C", "#FDBF6F", "#FF7F00", "#CAB2D6", "#6A3D9A", "#FFFF99", "#B15928")) +
  ggtitle("All UNSAT results") +
  xlab("CPU Time (in seconds)") +
  ylab("Number of problems solved") 

ggplot(sat_timings_kissat, aes(x = time, y = value, color=variable)) + 
  geom_line() +
  scale_color_manual(values=c("#A6CEE3", "#1F78B4", "#B2DF8A", "#33A02C", "#FB9A99", "#E31A1C", "#FDBF6F", "#FF7F00", "#CAB2D6", "#6A3D9A", "#FFFF99", "#B15928")) +
  ggtitle("SAT results using kissat for gate detection") +
  xlab("CPU Time (in seconds)") +
  ylab("Number of problems solved") 

ggplot(unsat_timings_kissat, aes(x = time, y = value, color=variable)) + 
  geom_line() +
  scale_color_manual(values=c("#A6CEE3", "#1F78B4", "#B2DF8A", "#33A02C", "#FB9A99", "#E31A1C", "#FDBF6F", "#FF7F00", "#CAB2D6", "#6A3D9A", "#FFFF99", "#B15928")) +
  ggtitle("UNSAT results using kissat for gate detection") +
  xlab("CPU Time (in seconds)") +
  ylab("Number of problems solved") 

ggplot(sat_timings_cnftools, aes(x = time, y = value, color=variable)) + 
  geom_line() +
  scale_color_manual(values=c("#A6CEE3", "#1F78B4", "#B2DF8A", "#33A02C", "#FB9A99", "#E31A1C", "#FDBF6F", "#FF7F00", "#CAB2D6", "#6A3D9A", "#FFFF99", "#B15928")) +
  ggtitle("SAT results using cnftools for gate detection") +
  xlab("CPU Time (in seconds)") +
  ylab("Number of problems solved") 

ggplot(unsat_timings_cnftools, aes(x = time, y = value, color=variable)) + 
  geom_line() +
  scale_color_manual(values=c("#A6CEE3", "#1F78B4", "#B2DF8A", "#33A02C", "#FB9A99", "#E31A1C", "#FDBF6F", "#FF7F00", "#CAB2D6", "#6A3D9A", "#FFFF99", "#B15928")) +
  ggtitle("UNSAT results using cnftools for gate detection") +
  xlab("CPU Time (in seconds)") +
  ylab("Number of problems solved")