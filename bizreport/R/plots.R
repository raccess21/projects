library(ggplot2)
library(rlang)

#' Create a Column/Bar Graph from Data
#' 
#' This function generates a column (bar) graph using `ggplot2` based on the provided data frame. The function 
#' allows dynamic selection of the x and y axes by using the first two columns in the data frame, or custom axis 
#' labels and title. The plot is then saved as a PNG image using the `saveGraph` function. Saves the generated column/bar graph as a PNG file in the "reports" directory. The file is named using the 
#'   plot's title and includes a random string to ensure uniqueness.
#' 
#' @param sdata A data frame or tibble containing the data for the graph. The first column is used for the x-axis 
#'   and the second column is used for the y-axis.
#' @param xname A character string to specify the label for the x-axis. If not provided (default is `FALSE`), the 
#'   label will be the name of the first column.
#' @param yname A character string to specify the label for the y-axis. If not provided (default is `FALSE`), the 
#'   label will be the name of the second column.
#' @param tname A character string to specify the title of the plot. If not provided (default is `""`), the title 
#'   will be generated using the names of the first two columns, formatted as "Column1 / Column2 Analysis".
#' @param fname A character string to specify the name of the save graph file. 
#' @return The plot that was created.
#' @import ggplot2
#' @import rlang
#' 
#' @examples
#' # Example data frame for creating a column graph
#' df <- tibble(Category = c("A", "B", "C"), Value = c(10, 20, 30))
#' columnGraph(df, xname = "Category", yname = "Value", tname = "Category Analysis")
#' 
#' # Example of creating a graph with default labels and title
#' columnGraph(df)
#' 
#' @export
columnGraph <- function(sdata, xname=FALSE, yname=FALSE, tname="", fname="") {
  # extract x and y column name from dataframe column 1 and 2 respectively
  colx <- colnames(sdata[1])
  coly <- colnames(sdata[2])
  
  # dynamically select aes x -> col 1, aes y -> col 2 of dataframe
  p <- ggplot(sdata, aes(x = .data[[colx]], y = .data[[coly]])) +  
    geom_col(aes(fill = .data[[coly]]), show.legend = FALSE) +
    #scale_fill_viridis_d("Kanda") +
    #scale_y_continuous(limits = c(0, 250)) +
    
    # defaults label name to name of columns
    labs(
      x = ifelse(isFALSE(xname), colx, xname),
      y = ifelse(isFALSE(yname), coly, yname),
      title = ifelse(tname == "", paste(colx, "/", coly, "Analysis"), tname)
    ) +
    theme_dark()
  
  fname <- saveGraph(p, fname)
  return(list("fname" = fname, "plot" = p))
}
