library(dplyr)
library(rlang)

#' Summarize and Organize Profit or Losses by Order Size
#'
#' This function organizes profit or loss by the size of the order, grouping the data by the `Range` column. It uses the 
#' `saleOrReturn` function to filter the data based on the `profits` argument. Profits are determined by whether the 
#' quantity is greater than 0, and losses are determined when quantity is less than 0. 
#' 
#' @param data A DataFrame or tibble containing the sales or return data, with columns for `Quantity` and `Amount`.
#' @param profits A logical value indicating whether to filter for profits (`TRUE`, default) or losses (`FALSE`). 
#'   Profits are based on data where the quantity is greater than 0, and losses are based on data where the quantity is less than 0.
#' 
#' @return A DataFrame or tibble with summarized profit or loss data, grouped by the `Range` column, where the value 
#'   reflects either `Profits` or `Losses` based on the `profits` argument.
#' 
#' @examples
#' df <- tibble(Range = c("0-10", "10-100", "0-10", "100-1000"),
#'              Quantity = c(10, -5, 20, -2),
#'              Amount = c(1000, -500, 2000, -200))
#' 
#' # Get profits by range
#' profit_result <- bulkOrderQuantity(df, profits = TRUE)
#' print(profit_result)
#' 
#' # Get losses by range
#' loss_result <- bulkOrderQuantity(df, profits = FALSE)
#' print(loss_result)
#' 
#' @export
bulkOrderQuantity <- function(data, profits=TRUE) {    
  # for profits true subset data where quantity greater than 0
  returns <- !profits
  datas <- saleOrReturn(data, returns, name1="Losses", name2="Profits")
  
  fdata <- datas$data |>
    group_by(Range) |>
    summarise(!!datas$rname := sum(Amount, na.rm=TRUE))
}
