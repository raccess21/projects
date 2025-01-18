out_directory <- "reports" 
if (!dir.exists(out_directory)) {
  dir.create(out_directory)
}

#stockCodeData <- stockCodeSale(data, num=5, decreasing = FALSE)
#columnGraph(stockCodeData)

#countrySaleData <- countrySale(data, num=5, decreasing = TRUE)
#columnGraph(countrySaleData)

#stockCodeProfitData <- stockCodeProfit(data, num=5, decreasing = TRUE)
#columnGraph(stockCodeProfitData)

#bulkOrderData <- bulkOrderQuantity(data, decreasing = TRUE, profits=TRUE)

bulkOrderData <- bulkOrderQuantity(data, decreasing = TRUE, profits=TRUE)