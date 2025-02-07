% Generated by roxygen2: do not edit by hand
% Please edit documentation in R/stockCodeAnalysis.R
\name{stockCodeProfit}
\alias{stockCodeProfit}
\title{Calculate Profits and Losses for Each Stock Code}
\usage{
stockCodeProfit(data, num, decreasing = TRUE)
}
\arguments{
\item{data}{A DataFrame or tibble containing the sales or return data, with columns for `StockCode` and `Amount`.}

\item{num}{An integer representing the number of top or bottom countries to return based on the total quantity. 
If `num` is negative, the bottom `abs(num)` countries will be returned.}

\item{decreasing}{A logical value indicating whether to sort the result in descending order (`TRUE`, default) 
or ascending order (`FALSE`).}
}
\value{
A DataFrame or tibble with the top `num` stock codes sorted by total profit or loss.
}
\description{
This function calculates the total profits or losses for each stock code by summing the `Amount` column for 
each stock code in the provided dataset. The results are sorted and the top `num` stock codes are returned, 
based on the total profit or loss. The results can be sorted in ascending or descending order, depending on the 
`decreasing` argument.
}
\examples{
df <- tibble(StockCode = c("A1", "B2", "A1", "B2", "C3"),
             Amount = c(100, -50, 200, -30, 150))
stock_code_profit_result <- stockCodeProfit(df, num = 2)
print(stock_code_profit_result)

}
