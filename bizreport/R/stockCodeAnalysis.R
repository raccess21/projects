library(dplyr)


#' Calculate Total Sale Quantity for Each Stock Code
#' 
#' This function calculates the total quantity of sales or returns for each stock code in the provided dataset. 
#' It uses the `saleOrReturn` function to filter the data based on whether sales or returns are being considered, 
#' and then groups the data by stock code to compute the total quantity. The result is sorted and the top `num` stock 
#' codes are returned, based on the total quantity. The results are either in ascending or descending order, depending 
#' on the `decreasing` argument.
#' 
#' @param data A DataFrame or tibble containing the sales or return data, with columns for `StockCode` and `Quantity`.
#' @param num An integer representing the number of top or bottom countries to return based on the total quantity. 
#'   If `num` is negative, the bottom `abs(num)` countries will be returned.
#' @param decreasing A logical value indicating whether to sort the result in descending order (`TRUE`, default) 
#'   or ascending order (`FALSE`).
#' @param returns A logical value indicating whether to filter for returns (`TRUE`) or sales (`FALSE`). Defaults to `FALSE` (sales).
#' 
#' @return A DataFrame or tibble with the top `num` stock codes sorted by total quantity, with the column name 
#'   reflecting either "TotalReturns" or "TotalSales" based on the `returns` argument.
#' @import tidyr
#' @examples
#' df <- tibble(StockCode = c("A1", "B2", "A1", "B2", "C3"),
#'              Quantity = c(10, -5, 20, -2, 15))
#' stock_code_sales_result <- stockCodeSales(df, num = 2, returns = TRUE)
#' print(stock_code_sales_result)
#' 
#' @export
stockCodeSales <- function(data, num, decreasing = TRUE, returns = FALSE) {
  if(num < 0) {
    num <- abs(num)
    decreasing <- !decreasing
  }
  
  datas <- saleOrReturn(data, returns, name1="TotalReturns", name2="TotalSales")

  datas$data |>
    group_by(StockCode) |>
    summarise(TotalQuantity = sum(abs(Quantity), na.rm = TRUE)) |>
    sortDataframe("TotalQuantity", decreasing) |>
    slice_head(n = num) |>
    rename(!!datas$rname := TotalQuantity)
}


#' Calculate Profits and Losses for Each Stock Code
#' 
#' This function calculates the total profits or losses for each stock code by summing the `Amount` column for 
#' each stock code in the provided dataset. The results are sorted and the top `num` stock codes are returned, 
#' based on the total profit or loss. The results can be sorted in ascending or descending order, depending on the 
#' `decreasing` argument.
#' 
#' @param data A DataFrame or tibble containing the sales or return data, with columns for `StockCode` and `Amount`.
#' @param num An integer representing the number of top or bottom countries to return based on the total quantity. 
#'   If `num` is negative, the bottom `abs(num)` countries will be returned.
#' @param decreasing A logical value indicating whether to sort the result in descending order (`TRUE`, default) 
#'   or ascending order (`FALSE`).
#' 
#' @return A DataFrame or tibble with the top `num` stock codes sorted by total profit or loss.
#' 
#' @examples
#' df <- tibble(StockCode = c("A1", "B2", "A1", "B2", "C3"),
#'              Amount = c(100, -50, 200, -30, 150))
#' stock_code_profit_result <- stockCodeProfit(df, num = 2)
#' print(stock_code_profit_result)
#' 
#' @export
stockCodeProfit <- function(data, num, decreasing = TRUE) {
  if(num < 0) {
    num <- abs(num)
    decreasing <- !decreasing
  }
  
  data |>
    group_by(StockCode) |>
    summarise(TotalProfit = sum(Amount, na.rm = TRUE)) |>
    sortDataframe("TotalProfit", decreasing) |>
    slice_head(n = num)
}


#' Generate Stock Code Pairs and Their Counts
#'
#' This function takes a dataset of transactions and generates unique stock code pairs 
#' for each invoice, along with the number of times each pair occurs across all invoices. 
#' Duplicate counts (e.g., "A-B" and "B-A") are handled by ensuring pairs are counted only once.
#'
#' @param data A data frame containing transaction data. Must include at least two columns:
#'   \describe{
#'     \item{\code{InvoiceNo}}{A column indicating invoice numbers.}
#'     \item{\code{StockCode}}{A column containing stock codes for each transaction.}
#'   }
#'
#' @return A data frame with two columns:
#'   \describe{
#'     \item{\code{pairs}}{Unique stock code pairs in the format "StockCode1-StockCode2".}
#'     \item{\code{PairCount}}{The number of times each pair appears across all invoices.}
#'   }
#'
#' @details
#' The function processes the data as follows:
#' - Groups transactions by invoice.
#' - Identifies unique stock codes within each invoice.
#' - Generates all possible pairs of stock codes for each invoice, ensuring that "A-B" and "B-A" are treated as the same pair.
#' - Calculates the total count for each unique pair across all invoices.
#'
#' @examples
#' # Example dataset
#' transactions <- data.frame(
#'   InvoiceNo = c(1, 1, 1, 2, 2),
#'   StockCode = c("A", "B", "C", "A", "B")
#' )
#'
#' # Generate stock pairs and their counts
#' stockPairs(transactions)
#'
#' @export
stockPairs <- function(data) {
  data |>
    group_by(InvoiceNo) |>
    summarise(StockCode1 = list(unique(StockCode)), .groups = "drop") |>
    unnest(StockCode1) |>
    group_by(InvoiceNo) |>
    mutate(StockCode2 = list(StockCode1), .groups = "drop") |>
    unnest(StockCode2) |>
    filter(StockCode1 != StockCode2) |>
    mutate(
      pairs = ifelse (StockCode1 < StockCode2, 
                      paste(StockCode1, StockCode2, sep = "-"), 
                      paste(StockCode2, StockCode1, sep = "-")
      ) 
    ) |>
    group_by(pairs) |>
    summarise(PairCount = n() / 2, .groups = "drop")
}


#' Extract Top Stock Codes Likely to Be Added to Basket
#'
#' This function identifies the most frequent stock codes that are likely to be added to the basket,
#' based on their association with a specified set of stock codes. The function works by filtering 
#' the pair data for the specified stock codes, excluding pairs that include the stock codes themselves,
#' then summarizing the pair counts, and returning the top `num` stock codes based on frequency.
#' The results can be sorted in either ascending or descending order based on the `num` parameter.
#'
#' @param pairData A data frame containing stock code pairs and their frequencies. 
#'   The data frame must include the following columns:
#'   \describe{
#'     \item{\code{pairs}}{A column containing stock code pairs in the format "StockCode1-StockCode2".}
#'     \item{\code{PairCount}}{A column containing the frequency of each pair.}
#'   }
#' @param codes A character vector containing the stock codes of interest. These stock codes will be used
#'   to filter the pairs and to exclude them from the results.
#' @param num An integer specifying the number of top stock codes to return. If positive, the function 
#'   returns the top `num` stock codes in descending order of `PairCount`. If negative, it returns the top 
#'   `num` stock codes in ascending order of `PairCount`. Defaults to 1.
#'
#' @return A character vector of stock codes that are most likely to be added to the basket, based on their 
#'   association with the specified stock codes. The results are ordered by `PairCount`, and the original 
#'   stock codes provided in the `codes` argument are excluded.
#'
#' @details
#' The function works as follows:
#' - Filters the data frame to retain only rows where the `pairs` column contains at least one of the 
#'   specified `codes`.
#' - Excludes rows where the stock codes in the pair are the same as any of the `codes` provided.
#' - Groups by the stock codes that are not in the `codes` list, summarizing the total count of their 
#'   pairings across all rows.
#' - Sorts the results based on the total pair count and returns the top `num` stock codes.
#'
#' @examples
#' # Example dataset
#' pairData <- data.frame(
#'   pairs = c("A-B", "A-C", "B-C", "C-D", "D-E", "A-D"),
#'   PairCount = c(10, 15, 5, 8, 3, 12)
#' )
#'
#' # Find the top 2 stock codes most likely to be added to the basket with "A"
#' stockCodeBaskets(pairData, codes = "A", num = 2)
#'
#' # Find the top 1 stock code most likely to be added to the basket with "A" and "B"
#' stockCodeBaskets(pairData, codes = c("A", "B"), num = 1)
#'
#' @export
stockCodesBasket <- function(pairData, codes, num = 1) {
  codes <- c(codes)
  decreasing <- ifelse(num > 0, TRUE, FALSE)
  num <- abs(num)

  basket <- pairData |>
    filter(stringr::str_detect(pairs, paste(codes, collapse = "|"))) |>
    separate(pairs, into = c("StockCode1", "StockCode2"), sep = "-") |>
    mutate(stockCodes = ifelse(StockCode1 %in% codes, StockCode2, StockCode1)) |>
    filter(!stockCodes %in% codes) |>
    group_by(stockCodes) |>
    summarise(PairCount = sum(PairCount), .groups = "drop") |>
    sortDataframe("PairCount", decreasing) |>
    slice_head(n = num)

  return(as.character(basket$stockCodes))
}
