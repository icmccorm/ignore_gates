library(ggplot2)
library(tidyverse)
library(dplyr)
library(openxlsx)
library(RColorBrewer)
library(gridExtra)
library(tikzDevice)
library(ggpubr)
options(tz="CA")

# thanks, https://sashamaps.net/docs/resources/20-colors/!
PALETTE = c("#e6194B", "#3cb44b", "#000075", "#4363d8", "#f58231", "#911eb4", "#9A6324", "#800000", "#808000", "#bfef45", "#469990", "#f032e6", "#42d4f4", "#000000")
MANUAL = c(
    "control" = "#A6CEE3",
    "control.noelim" = "#1F78B4",
    "control.sideeffects" = "#42d4f4",
    "control.lastuip" = "#000000",
    "kissat.br" = "#B2DF8A", 
    "kissat.br.elim" = "#33A02C",
    "kissat.br.elim.uip" = "#FB9A99",
    "kissat.br.uip" = "#E31A1C",
    "kissat.elim" = "#FDBF6F",
    "cnftools.br" = "#FF7F00",
    "cnftools.br.elim" = "#CAB2D6",
    "cnftools.br.elim.uip" = "#6A3D9A",
    "cnftools.br.uip" = "#FFFF99",
    "cnftools.elim" = "#B15928"    
)

sat_timings <- read.csv(file = './results/sat_timed.csv')
unsat_timings <- read.csv(file = './results/unsat_timed.csv')
sat_timings <- sat_timings[,!(names(sat_timings) %in% c("X"))]
unsat_timings <- unsat_timings[,!(names(unsat_timings) %in% c("X"))]

sat_timings_kissat <- select(sat_timings, !contains("cnftools")) %>% gather(key = "variable", value = "value", -time) %>% mutate(variable = fct_reorder(variable, value, tail, n = 1, .desc = TRUE))
sat_timings_cnftools <- select(sat_timings, !contains("kissat")) %>% gather(key = "variable", value = "value", -time) %>% mutate(variable = fct_reorder(variable, value, tail, n = 1, .desc = TRUE))

unsat_timings_kissat <- select(unsat_timings, !contains("cnftools")) %>% gather(key = "variable", value = "value", -time) %>% mutate(variable = fct_reorder(variable, value, tail, n = 1, .desc = TRUE))
unsat_timings_cnftools <- select(unsat_timings, !contains("kissat")) %>% gather(key = "variable", value = "value", -time) %>% mutate(variable = fct_reorder(variable, value, tail, n = 1, .desc = TRUE))

sat_timings <- sat_timings %>% gather(key = "variable", value = "value", -time) %>% mutate(variable = fct_reorder(variable, value, tail, n = 1, .desc = TRUE))
unsat_timings <- unsat_timings %>% gather(key = "variable", value = "value", -time) %>% mutate(variable = fct_reorder(variable, value, tail, n = 1, .desc = TRUE))


g_all_sat<-ggplot(sat_timings, aes(x = time, y = value, color = variable)) + 
  geom_line() +
  scale_color_manual(values=PALETTE) +
  xlab("CPU Time") +
  ylab("solved instances (SAT)") +
  theme(legend.position = "none") +
  theme(panel.border = element_rect(fill=NA,color="black", size=0.5, 
                                    linetype="solid")) +
  guides(colour = guide_legend(override.aes = list(size=4)))


g_all_unsat <- ggplot(unsat_timings, aes(x = time, y = value, color=variable)) + 
  geom_line() +
  scale_color_manual(values=PALETTE) +
  xlab("CPU Time") +
  ylab("solved instances (UNSAT)") +
  theme(panel.border = element_rect(fill=NA,color="black", size=0.5, 
                                    linetype="solid")) +
  guides(colour = guide_legend(override.aes = list(size=4)))

g_sat_kissat <- ggplot(sat_timings_kissat, aes(x = time, y = value, color=variable)) + 
  geom_line() +
  scale_color_manual(values=c(
    "control" = "#A6CEE3",
    "control.noelim" = "#1F78B4",
    "control.sideeffects" = "#42d4f4",
    "control.lastuip" = "#000000",
    "kissat.br" = "#B2DF8A", 
    "kissat.br.elim" = "#33A02C",
    "kissat.br.elim.uip" = "#FB9A99",
    "kissat.br.uip" = "#E31A1C",
    "kissat.elim" = "#FDBF6F",
    "cnftools.br" = "#FF7F00",
    "cnftools.br.elim" = "#CAB2D6",
    "cnftools.br.elim.uip" = "#6A3D9A",
    "cnftools.br.uip" = "#FFFF99",
    "cnftools.elim" = "#B15928"    
  )) +
  ggtitle("SAT results using kissat for gate detection") +
  xlab("CPU Time") +
  ylab("solved instances (SAT)") +
  theme(panel.border = element_rect(fill=NA,color="black", size=0.5, 
                                    linetype="solid"))

g_unsat_kissat <- ggplot(unsat_timings_kissat, aes(x = time, y = value, color=variable)) + 
  geom_line() +
  scale_color_manual(values=c(
    "control" = "#A6CEE3",
    "control.noelim" = "#1F78B4",    
    "control.sideeffects" = "#42d4f4",
    "control.lastuip" = "#000000",
    "kissat.br" = "#B2DF8A", 
    "kissat.br.elim" = "#33A02C",
    "kissat.br.elim.uip" = "#FB9A99",
    "kissat.br.uip" = "#E31A1C",
    "kissat.elim" = "#FDBF6F"
  )) +
  ggtitle("UNSAT results using kissat for gate detection") +
  xlab("CPU Time") +
  ylab("solved instances (UNSAT)") +
  theme(panel.border = element_rect(fill=NA,color="black", size=0.5, 
                                    linetype="solid"))

g_sat_cnf <- ggplot(sat_timings_cnftools, aes(x = time, y = value, color=variable)) + 
  geom_line() +
  scale_color_manual(values=c(
    "control" = "#A6CEE3",
    "control.noelim" = "#1F78B4",
    "control.sideeffects" = "#42d4f4",
    "control.lastuip" = "#000000",
    "cnftools.br" = "#FF7F00",
    "cnftools.br.elim" = "#CAB2D6",
    "cnftools.br.elim.uip" = "#6A3D9A",
    "cnftools.br.uip" = "#FFFF99",
    "cnftools.elim" = "#B15928"
  )) +
  ggtitle("SAT results using cnftools for gate detection") +
  xlab("CPU Time") +
  ylab("solved instances (SAT)")  +
  theme(panel.border = element_rect(fill=NA,color="black", size=0.5, 
                                    linetype="solid"))

g_unsat_cnf <- ggplot(unsat_timings_cnftools, aes(x = time, y = value, color=variable)) + 
  geom_line() +
  scale_color_manual(values=c(
    "control" = "#A6CEE3",
    "control.noelim" = "#1F78B4",
    "control.sideeffects" = "#42d4f4",
    "control.lastuip" = "#000000",
    "cnftools.br" = "#FF7F00",
    "cnftools.br.elim" = "#CAB2D6",
    "cnftools.br.elim.uip" = "#6A3D9A",
    "cnftools.br.uip" = "#FFFF99",
    "cnftools.elim" = "#B15928"
  )) +
  ggtitle("UNSAT results using cnftools for gate detection") +
  xlab("CPU time") +
  ylab("solved instances (UNSAT)") +
  theme(panel.border = element_rect(fill=NA,color="black", size=0.5, 
                                    linetype="solid"))

tikz(file = "plots.tex", width = 6, height = 8)
ggarrange(g_all_sat, g_all_unsat, ncol=1, nrow=2, common.legend = FALSE, legend="right")
