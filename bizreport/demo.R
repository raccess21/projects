library(bizreport)

filename <- "asset/online_retail.csv.gz"
data <- loadData(filename)
  
bulkOrderQuantityData <- bulkOrderQuantity(data, profits = TRUE)

countrySaleData <- countrySale(data, 5, returns = FALSE)
columnGraphData <- columnGraph(countrySaleData, fname = "graphie")

stockCodeProfitData <- stockCodeProfit(data, 5)
stockCodeSalesData <- stockCodeSales(data, 5, returns = FALSE)
#stockPairsData <- stockPairs(data)
stockCodesBasketData <- stockPairsData |>
  stockCodesBasket("22565", num = 5)
