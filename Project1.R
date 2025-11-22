library(tidyverse)
library(ggplot2)

ChickFilA <- read_csv("Project1dta.csv") %>%
  mutate_at("Response #",factor)

ggplot(ChickFilA, aes(x= `Chick-Fil-A Sauce`)) +
  geom_bar(fill="royalblue")+ 
  labs(
    x="Likes Chick-Fil-A Sauce",
    y="Count",
    title = "Do BYU students that lunch at the Wilkinson center like Chick Fil A Sauce?",
    subtitle = "2025 small survey"
  )

chisq.test(ChickFilA$`Chick-Fil-A Sauce`,ChickFilA$Utah)


#With the data acquired, there isn't a statistically significant correlation between being 
#from Utah and liking Chick Fil A Sauce, since the p-value is above the significance
#level of 0.05. 

#Most of the interviewed BYU students that had lunch at the Wilkinson Center 
#liked Chick Fil A Sauce


