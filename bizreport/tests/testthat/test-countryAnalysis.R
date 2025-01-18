library(tibble)

file_name <- "../../asset/online_retail.csv.gz"
data <- loadData(file_name)

# most and least sales for countries
mostSale <- tibble(
  Country = "United Kingdom",
  TotalSales = 4269472
)

leastSale <- tibble(
  Country = "Saudi Arabia",
  TotalSales = 80
)

test_that("coutrySales for most sales", {
  expect_equal(countrySale(data, 1), mostSale)
})

test_that("coutrySales for least sales", {
  expect_equal(countrySale(data, 1, decreasing=FALSE), leastSale)
  
})


# Most and least returns for countries
mostReturn <- tibble(
  Country = "United Kingdom",
  TotalReturns = 260939
)

leastReturn <- tibble(
  Country = "Greece",
  TotalReturns = 1
)

test_that("countrySale with most returns", {
  expect_equal(countrySale(data, 1, decreasing=TRUE, returns=TRUE), mostReturn)
})

test_that("countrySale with least returns", {
  expect_equal(countrySale(data, 1, decreasing=FALSE, returns=TRUE), leastReturn)
})

test_that("countrySale with least returns without passing decreasing", {
  expect_equal(countrySale(data, 1, returns=TRUE), mostReturn)
})