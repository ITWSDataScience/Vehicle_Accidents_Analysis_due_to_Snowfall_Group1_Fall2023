library(ggplot2)
library(corrplot)
library(reshape2)

data <- read.csv("clean_iqr.csv")
View(data)

names(data) <- c("ID", "Rainfall_Q1", "Rainfall_Q2", 
                 "Rainfall_Q3", "Rainfall_Q4", 
                 "Temperature_Q1", "Temperature_Q2",
                 "Temperature_Q3", "Temperature Quarter 4")
View(data)
attach(data)

# Summary Statistics
summary(data[,-1])

# Calculate correlation matrix
correlation_matrix <- cor(data[, -1]) 
print(correlation_matrix)
corrplot(correlation_matrix, method = "color")

# Histogram
hist(Rainfall_Q1, main = "Rainfall - Quarter 1")
hist(Rainfall_Q2, main = "Rainfall - Quarter 2")
hist(Rainfall_Q3, main = "Rainfall - Quarter 3")
hist(Rainfall_Q4, main = "Rainfall - Quarter 4")

hist(Temperature_Q1, main = "Temperature - Quarter 1")
hist(Temperature_Q2, main = "Temperature - Quarter 2")
hist(Temperature_Q3, main = "Temperature - Quarter 3")
hist(Temperature_Q4, main = "Temperature - Quarter 4")

# Kernel Density Plot
ggplot(data, aes(x = Rainfall_Q1)) +
  geom_density(fill = "skyblue", alpha = 0.7) +
  labs(title = "Kernel Density Plot - Rainfall Quarter 1", 
       x = "Rainfall", y = "Density")

ggplot(data, aes(x = Rainfall_Q2)) +
  geom_density(fill = "skyblue", alpha = 0.7) +
  labs(title = "Kernel Density Plot - Rainfall Quarter 2", 
       x = "Rainfall", y = "Density")

ggplot(data, aes(x = Rainfall_Q3)) +
  geom_density(fill = "skyblue", alpha = 0.7) +
  labs(title = "Kernel Density Plot - Rainfall Quarter 3", 
       x = "Rainfall", y = "Density")

ggplot(data, aes(x = Rainfall_Q4)) +
  geom_density(fill = "skyblue", alpha = 0.7) +
  labs(title = "Kernel Density Plot - Rainfall Quarter 4", 
       x = "Rainfall", y = "Density")


ggplot(data, aes(x = Temperature_Q1)) +
  geom_density(fill = "lightgreen", alpha = 0.7) +
  labs(title = "Kernel Density Plot - Temperature Quarter 1", 
       x = "Temperature", y = "Density")

ggplot(data, aes(x = Temperature_Q2)) +
  geom_density(fill = "lightgreen", alpha = 0.7) +
  labs(title = "Kernel Density Plot - Temperature Quarter 2", 
       x = "Temperature", y = "Density")

ggplot(data, aes(x = Temperature_Q3)) +
  geom_density(fill = "lightgreen", alpha = 0.7) +
  labs(title = "Kernel Density Plot - Temperature Quarter 3", 
       x = "Temperature", y = "Density")

ggplot(data, aes(x = Temperature_Q4)) +
  geom_density(fill = "lightgreen", alpha = 0.7) +
  labs(title = "Kernel Density Plot - Temperature Quarter 4", 
       x = "Temperature", y = "Density")


# Melt the data for easier plotting
melted_data <- melt(data, id.vars = "ID")

# Plotting average rainfall trends across quarters for different schools
ggplot(melted_data[melted_data$variable %in% 
                     c("Rainfall_Q1", "Rainfall_Q2", "Rainfall_Q3", "Rainfall_Q4"), ],
       aes(x = variable, y = value, group = ID, color = ID)) + geom_line() + 
  labs(title = "Average Rainfall Trends Across Quarters", 
       x = "Quarter", y = "Rainfall") + theme_minimal()

# Plotting average temperature trends across quarters for different schools
ggplot(melted_data[melted_data$variable %in% 
                     c("Temperature_Q1", "Temperature_Q2", 
                       "Temperature_Q3", "Temperature_Q4"), ],
       aes(x = variable, y = value, group = ID, color = ID)) + 
  geom_line() + labs(title = "Average Temperature Trends Across Quarters", 
                     x = "Quarter", y = "Temperature") + theme_minimal()

