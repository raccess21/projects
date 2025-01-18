# sortDataFrame test
data <- tibble(
  InvoiceNo = c("536365", "536365", "536365"),
  Quantity = c(6, 8, 9)
)

dataAsc <- tibble(
  InvoiceNo = c("536365", "536365", "536365"),
  Quantity = c(6, 8, 9)
)

dataDesc <- tibble(
  InvoiceNo = c("536365", "536365", "536365"),
  Quantity = c(9, 8, 6)
)

test_that("sortDataframe descending sort", {
  expect_equal(sortDataframe(data, "Quantity"), dataDesc)
})

test_that("sortDataframe ascending sort", {
  expect_equal(sortDataframe(data, "Quantity", decreasing = FALSE), dataAsc)
})


# saleOrReturn test
data <- tibble(
  InvoiceNo = c("536365", "536365", "536365"),
  Quantity = c(6, -8, 9)
)

sale <- tibble(
  InvoiceNo = c("536365", "536365"),
  Quantity = c(6, 9)
)

test_that("saleOrReturn for returns false", {
  result <- saleOrReturn(data, returns = FALSE)
  expect_equal(result$data, sale)
})

test_that("saleOrReturn for returns true", {
  result <- saleOrReturn(data, returns = TRUE, name1="Bach", name2="Litchi")
  expect_equal(result$rname, "Bach")
})