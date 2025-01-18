library(testthat)
library(dplyr)

# Sample Data for Testing
pairData <- data.frame(
  pairs = c("A-B", "A-C", "B-C", "C-D", "D-E", "A-D"),
  PairCount = c(10, 15, 5, 8, 3, 12)
)

# Test 1: Basic functionality check
test_that("stockCodesBasket returns correct stockCodes", {
  result <- stockCodesBasket(pairData, codes = "A", num = 2)
  expect_equal(result, c("C", "D"))
})

# Test 2: Check for number of results based on `num`
test_that("stockCodesBasket returns the correct number of stockCodes based on num", {
  result <- stockCodesBasket(pairData, codes = "A", num = 1)
  expect_equal(result, "C")  # Since only one pair is requested
  
  result <- stockCodesBasket(pairData, codes = "A", num = -2)
  expect_equal(result, c("B", "D"))  # Sorted in ascending order of PairCount
})

# Test 3: Edge case where no pair exists
test_that("stockCodesBasket handles cases where no pairs are found", {
  result <- stockCodesBasket(pairData, codes = "F", num = 2)
  expect_equal(result, character(0))  # No stock codes found for 'F'
})

# Test 4: Ensure the `codes` are excluded from the output
test_that("stockCodesBasket excludes the provided codes from the output", {
  result <- stockCodesBasket(pairData, codes = c("A", "B"), num = 2)
  expect_equal(result, c("C", "D"))  # A and B should not be in the result
})

# Test 5: Ensure that `num` works with positive and negative values
test_that("stockCodesBasket handles positive and negative num correctly", {
  result <- stockCodesBasket(pairData, codes = "A", num = 1)
  expect_equal(result, "C")  # Should return the most frequent pair
  
  result <- stockCodesBasket(pairData, codes = "A", num = -1)
  expect_equal(result, "B")  # Sorted in ascending order, thus D comes first
})
