library(dplyr)
library(ggvis)
library(ggplot2)
library(psych)
library(car)

entries_hourly <- select(turnstile_weather_v2, ENTRIESn_hourly, rain) %>%
  filter(ENTRIESn_hourly < 6000)

mean_entries <- group_by(entries_hourly, rain) %>%
  summarise(entries.median = median(ENTRIESn_hourly))
  

entries_hist <- ggplot(entries_hourly, aes(x = ENTRIESn_hourly, fill = as.factor(rain))) + 
  geom_histogram(alpha = 0.5, position = "identity") +
  geom_vline(data = mean_entries, aes(xintercept = entries.median, color = as.factor(rain)),
                                      linetype = "dashed", size = 1) +
  ggtitle("Count of Entries Per Hour Rain vs. No Rain") + 
  xlab("Entries") +
  ylab("Count") +
  scale_fill_discrete(name = "Raining?",
                      breaks = c(0, 1),
                      labels = c("No Rain", "Rain"))

entries_summary <- by(entries_hourly$ENTRIESn_hourly, entries_hourly$rain, describe)

rain_levene <- leveneTest(entries_hourly$ENTRIESn_hourly, as.factor(entries_hourly$rain))