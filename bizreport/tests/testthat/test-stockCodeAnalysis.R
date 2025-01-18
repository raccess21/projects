library(tibble)

file_name <- "../../asset/online_retail.csv.gz"
data <- loadData(file_name)


# stockCodeSales test for sales
mostSale <- tibble(
  StockCode = "23843",
  TotalSales = 80995
)

leastSale <- tibble(
  StockCode = "20667",
  TotalSales = 1
)

test_that("stockCodeSales with most sales", {
  expect_equal(stockCodeSales(data, 1), mostSale)
})

test_that("stockCodeSales with least sales", {
  expect_equal(stockCodeSales(data, 1, decreasing=FALSE), leastSale)
})

# stockCodeSales test for returns
mostReturn <- tibble(
  StockCode = "23843",
  TotalReturns = 80995
)

leastReturn <- tibble(
  StockCode = "10135",
  TotalReturns = 1
)

test_that("Returns country with most returns", {
  expect_equal(stockCodeSales(data, 1, decreasing=TRUE, returns=TRUE), mostReturn)
})

test_that("Returns country with least returns", {
  expect_equal(stockCodeSales(data, 1, decreasing=FALSE, returns=TRUE), leastReturn)
})


# stockCodeProfit tests
mostProfit <- tibble(
  StockCode = "22423",
  TotalProfit = round( 132870.40, 2)
)

leastProfit <- tibble(
  StockCode = "M",
  TotalProfit = round(-58385.460, 2)
)

test_that("stockCodeProfit returns stock code with most profits", {
  result <- stockCodeProfit(data, 1)
  result$TotalProfit <- round(result$TotalProfit, 2)
  expect_equal(result, mostProfit)
})

test_that("stockCodeProfit returns stock code with least profits", {
  result <- stockCodeProfit(data, 1, decreasing=FALSE)
  result$TotalProfit <- round(result$TotalProfit, 2)
  expect_equal(result, leastProfit)
})