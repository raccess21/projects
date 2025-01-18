suppressPackageStartupMessages(library(tidyverse))

#' Load Data from CSV File
#'
#' This function loads a CSV file into a data frame or tibble. It automatically reads
#' the file and returns the contents.
#'
#' @param filename A character string representing the path to the CSV file to be loaded.
#' @return A tibble or data frame containing the data from the CSV file.
#' @import tidyverse
#' @import tibble
#' @import rlang
#' @import stringr
#' @import dplyr
#' @importFrom lubridate mdy_hm
#' @details
#' The function uses `read.csv()` or `readr::read_csv()` to load the CSV file and 
#' automatically handles common data loading scenarios such as missing values and 
#' incorrect data types.
#' @examples
#' # Load data from a CSV file
#' data <- loadData("path/to/your/file.csv")
#' # View the loaded data
#' head(data)
#' 
#' @export
loadData <- function(file_name=NULL) {
  if(is.null(file_name)) {
    return(FALSE)
  }
  
  data <- read.csv(file_name) |>
    subset(!is.na(InvoiceNo) & !is.na(StockCode) & !is.na(CustomerID)) |>
    mutate(
      InvoiceDate = lubridate::mdy_hm(InvoiceDate), 
      Amount = UnitPrice * Quantity,
    ) |>
    tibble()
  
  max_val <- nchar(as.character(max(data$Quantity))) + 1
  breaks <- c(0, 10^c(1:max_val))
  
  labels <- c()
  for (i in 2:length(breaks)) {
    labels <- c(labels, paste0(breaks[i-1], "-", breaks[i]))
  }
  
  data <- data |>
    mutate(Range = cut(abs(Quantity), breaks = breaks, labels = labels, right = FALSE))
}