test_that("loadData loads data correctly", {
  file_name <- "../../asset/online_retail.csv.gz"
  
  expect_false(loadData())
  expect_true(is_tibble(loadData(file_name)))
})