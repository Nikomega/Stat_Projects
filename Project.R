library(tidyverse)


Monkey <- read_csv("MTE Data(1).csv")

MTE_Data_1_$Block <- as_factor(MTE_Data_1_$Block)

MTE_Data_1_.lm <- lm(WPM ~ Block + Music + Quote , data=MTE_Data_1_)

anova(MTE_Data_1_.lm)

MTE_Data_1_ %>%
  group_by(Block) %>%
  summarize(mean(WPM))
