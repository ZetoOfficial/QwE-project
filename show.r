# load wordcloud2
library(wordcloud2)
options(browser = "google-chrome-stable")

# Make the graph
dataset <- read.csv("./skills.csv")
wordcloud2(data = dataset)