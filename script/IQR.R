# Remember to set working directory to correct folder

combined <- read.csv("combined_dataset.csv")
View(combined)

get_quarter <- function(data, months, name) {
  years <- as.character(seq(from = 2013, to = 2023))
  
  columns <- c('ID')
  
  # Loop through each year and month to find matching column names
  for (year in years) {
    for (month in months) {
      pattern <- paste0(name, '_', year, '_', month, '_')
      columns <- c(columns, grep(pattern, names(data), value = TRUE))
    }
  }
  
  subset_data <- data[, columns]
  
  names(subset_data) <- gsub("20[0-9]{2}", "", names(subset_data))
  
  return(subset_data)
}


# Filter and combine the data for specific months
q1 <- c('03','04','05')
q2 <- c('06','07','08')
q3 <- c('09','10','11')
q4 <- c('12','13','14')

name <- "rain"
rain_q1 <- get_quarter(combined, q1, name)
rain_q2 <- get_quarter(combined, q2, name)
rain_q3 <- get_quarter(combined, q3, name)
rain_q4 <- get_quarter(combined, q4, name)

name <- "temp"
temp_q1 <- get_quarter(combined, q1, name)
temp_q2 <- get_quarter(combined, q2, name)
temp_q3 <- get_quarter(combined, q3, name)
temp_q4 <- get_quarter(combined, q4, name)

View(rain_q1)

# summary(rain_q1)

iqr_outliers <- function(row) {
  n_row <- as.numeric(row)
  
  # Calculate the IQR
  iqr <- IQR(n_row, na.rm = TRUE)
  
  quan1 <- quantile(n_row, probs = 0.25)
  quan3 <- quantile(n_row, probs = 0.75)
  lower_fence <- quan1 - 1.5 * iqr
  upper_fence <- quan3 + 1.5 * iqr
  
  mean(n_row[n_row >= lower_fence & n_row <= upper_fence], na.rm = TRUE)
}

# Apply the function to each row excluding first row
cleaned_rain_q1 <- apply(rain_q1[,-1], 1, iqr_outliers)
cleaned_rain_q2 <- apply(rain_q2[,-1], 1, iqr_outliers)
cleaned_rain_q3 <- apply(rain_q3[,-1], 1, iqr_outliers)
cleaned_rain_q4 <- apply(rain_q4[,-1], 1, iqr_outliers)

new_rain_q1 <- data.frame(ID = rain_q1$ID, avg_rain_q1 = cleaned_rain_q1)
new_rain_q2 <- data.frame(ID = rain_q2$ID, avg_rain_q2 = cleaned_rain_q2)
new_rain_q3 <- data.frame(ID = rain_q3$ID, avg_rain_q3 = cleaned_rain_q3)
new_rain_q4 <- data.frame(ID = rain_q4$ID, avg_rain_q4 = cleaned_rain_q4)

cleaned_temp_q1 <- apply(temp_q1[,-1], 1, iqr_outliers)
cleaned_temp_q2 <- apply(temp_q2[,-1], 1, iqr_outliers)
cleaned_temp_q3 <- apply(temp_q3[,-1], 1, iqr_outliers)
cleaned_temp_q4 <- apply(temp_q4[,-1], 1, iqr_outliers)

new_temp_q1 <- data.frame(ID = temp_q1$ID, avg_temp_q1 = cleaned_temp_q1)
new_temp_q2 <- data.frame(ID = temp_q2$ID, avg_temp_q2 = cleaned_temp_q2)
new_temp_q3 <- data.frame(ID = temp_q3$ID, avg_temp_q3 = cleaned_temp_q3)
new_temp_q4 <- data.frame(ID = temp_q4$ID, avg_temp_q4 = cleaned_temp_q4)

# Merge the clean data into one 
dataset_list <- list(new_rain_q1, new_rain_q2, new_rain_q3, new_rain_q4, 
                     new_temp_q1, new_temp_q2, new_temp_q3, new_temp_q4)

merged_data <- dataset_list[[1]]

# Loop through the remaining datasets and merge based on 'ID'
for (i in 2:length(dataset_list)) {
  merged_data <- merge(merged_data, dataset_list[[i]], by = "ID", all = TRUE)
}

View(merged_data)

write.csv(merged_data, file = "clean_iqr.csv", row.names = FALSE)
