#' Summarize and Sort Sales or Returns by Country
#' 
#' This function summarizes the sales or returns data by country and sorts the total quantity in ascending or 
#' descending order. It uses the `saleOrReturn` function to filter data based on the `returns` argument and 
#' groups the results by country, summing the absolute quantity.
#' 
#' If `num` is negative, the function returns the bottom `abs(num)` countries based on total quantity in the 
#' opposite order (ascending if it was descending, and vice versa).
#' 
#' @param data A DataFrame or tibble containing the sales or return data, with columns for `Country` and `Quantity`.
#' @param num An integer representing the number of top or bottom countries to return based on the total quantity. 
#'   If `num` is negative, the bottom `abs(num)` countries will be returned.
#' @param decreasing A logical value indicating whether to sort the result in descending order (`TRUE`, default) 
#'   or ascending order (`FALSE`).
#' @param returns A logical value indicating whether to filter for returns (`TRUE`) or sales (`FALSE`). Defaults to `FALSE` (sales).
#' 
#' @return A DataFrame or tibble with the top or bottom `num` countries sorted by total quantity, with the column name 
#'   reflecting either "TotalReturns" or "TotalSales" based on the `returns` argument.
#' @import tidyverse
#' @examples
#' df <- tibble(Country = c("UK", "USA", "UK", "USA"),
#'              Quantity = c(10, -5, 20, -2))
#' # Get top 2 countries based on total sales
#' country_sale_result <- countrySale(df, num = 2, returns = FALSE)
#' print(country_sale_result)
#' 
#' # Get bottom 2 countries based on total sales
#' country_sale_result <- countrySale(df, num = -2, returns = FALSE)
#' print(country_sale_result)
#' 
#' @export
countrySale <- function(data, num, decreasing = TRUE, returns = FALSE) {
  if(num < 0) {
    num <- abs(num)
    decreasing <- !decreasing
  }
  
  datas <- saleOrReturn(data, returns, name1="TotalReturns", name2="TotalSales")

  data <- datas$data |>
    select(Country, Quantity) |>
    group_by(Country) |>
    summarise(TotalQuantity = sum(abs(Quantity), na.rm = TRUE)) |>
    sortDataframe("TotalQuantity", decreasing) |>
    slice_head(n = num) |>
    rename(!!datas$rname := TotalQuantity)
}
