library(rlang)
library(ggplot2)


#' Sort DataFrame by a Given Column
#'
#' This function sorts a data frame based on a specified column, in either ascending or descending order.
#'
#' @param data A DataFrame or tibble that you want to sort.
#' @param column A character string representing the column name to sort by.
#' @param decreasing A logical value. If `TRUE` (default), the data will be sorted in descending order, 
#'   otherwise, in ascending order.
#'
#' @return A sorted DataFrame or tibble based on the given column.
#' @import rlang
#' 
#' @examples
#' df <- tibble(StockCode = c("A1", "B2", "A1", "B2"),
#'              Amount = c(100, -50, 200, -30))
#' sorted_df <- sortDataframe(df, "Amount", decreasing = TRUE)
#' print(sorted_df)
#' 
#' @export
sortDataframe <- function(data, column, decreasing = TRUE) {
  if (!column %in% names(data)) {
    stop("The specified column does not exist in the data frame.")
  }
  
  col_sym <- sym(column)
  
  if (decreasing == TRUE) {
    data |>
      arrange(desc(!!col_sym))
  } else {
    data |>
      arrange(!!col_sym)
  }
}


#' Filter Sales or Returns Data Based on Quantity
#' 
#' This function filters the data based on the quantity. It selects rows with a quantity greater than 0 for sales 
#' or a quantity less than 0 for returns, depending on the value of the `returns` argument. The function also 
#' assigns a column name based on the specified `name1` and `name2` arguments.
#' 
#' @param data A DataFrame or tibble containing the sales or return data.
#' @param returns A logical value indicating whether to filter for returns (`TRUE`) or sales (`FALSE`).
#'   Defaults to `FALSE` (sales).
#' @param name1 A string representing the name to use for returns, defaults to "Returns".
#' @param name2 A string representing the name to use for sales, defaults to "Sales".
#' 
#' @return A list with two elements:
#'   \describe{
#'     \item{data}{A DataFrame or tibble filtered based on quantity (greater than 0 for sales, less than 0 for returns).}
#'     \item{rname}{A string representing the name of the category ("Returns" or "Sales").}
#'   }
#' 
#' @examples
#' df <- tibble(InvoiceNo = c(1, 2, 3, 4), Quantity = c(10, -5, 3, -2))
#' result <- saleOrReturn(df, returns = TRUE)
#' print(result$data)  # Rows where Quantity < 0 (returns)
#' print(result$rname)  # "Returns"
#' 
#' @export
saleOrReturn <- function(data, returns = FALSE, name1="Returns", name2="Sales") {
  
  if (isTRUE(returns)) {
    data <- data |>
      subset(Quantity < 0)
    rname <- name1  
  } else {
    data <- data |>
      subset(Quantity > 0)
    rname <- name2
  }

  return(list(data = data, rname = rname))
}


#' Save Plot as an Image File
#' 
#' This function saves a given ggplot2 plot as an image file in the "reports" directory. If no name is provided, 
#' the function will use the title of the plot as the default filename, with any spaces replaced by underscores 
#' and slashes replaced with "by". A random string is appended to the filename to ensure uniqueness.
#' 
#' If the "reports" directory does not exist, it will be created.
#' 
#' @param p A ggplot2 plot object to be saved.
#' @param fname A character string specifying the desired filename (without the file extension). 
#'   If not provided (default is `""`), the function will use the plot's title as the filename.
#' 
#' @return Location of saved plot.
#' @import ggplot2
#' 
#' @examples
#' # Example of saving a plot with a custom filename
#' p <- ggplot(mtcars, aes(x = wt, y = mpg)) + geom_point() + ggtitle("Car Weight vs MPG")
#' saveGraph(p, "custom_plot_name")
#' 
#' # Example of saving a plot with a default filename (based on the plot's title)
#' saveGraph(p)
#'
#' @export 
saveGraph <- function(p, fname = "") {
  if(!dir.exists("reports")) {
    dir.create("reports")
    message("Reports directory created for report export.")
  }
  
  
  if (fname == "") {
    random_string <- paste0(sample(c(letters, LETTERS, 0:9), 5, replace = TRUE), collapse = "")
    fname <- gsub(" ", "_", p$labels$title)
    fname <- gsub("/", "by", fname)
    fname <- paste0(fname, random_string)
  }
  
  fname <- paste0("reports/", fname, ".png")
  ggsave(
    fname,
    plot = p,
    height = 1200,
    width = 1200,
    units = "px"
  )

  cat(paste("Saved graph at", fname))
  return(fname)
}
