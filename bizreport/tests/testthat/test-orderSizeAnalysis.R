library(tibble)

file_name <- "../../asset/online_retail.csv.gz"
data <- loadData(file_name)

profit_data <- c(2680865, 4141018, 1680227, 163644, 245653)
loss_data <- c(-200708,  -67029,  -75314,  -22637, -245653)

test_that("Profits and losses grouped by ranges are correct for profits", {
  result <- bulkOrderQuantity(data, profits=TRUE)
  result <- round(result$Profits, 0)
  expect_equal(result, profit_data)
})

test_that("Profits and losses grouped by ranges are correct for losses", {
  result <- bulkOrderQuantity(data, profits=FALSE)
  result <- round(result$Losses, 0)
  expect_equal(result, loss_data)
})