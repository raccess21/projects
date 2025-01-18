library(magick)


#document size set in environment
#take a heading, chart image and conclusion and return a dataframe
create_element <- function(heading, chart, conclusion) {
  # Create a blank image for text pages
  heading <- image_blank(width = 1920, height = 100, color = "white") |>
    image_annotate(heading, size = 30, color = "black", location = "+30+20")
  
  # Read the image
  chart <- image_read(chart) |>
    image_resize("800x400!")  # Resize to 800x400 pixels
  
  offset <- paste0("+", (width-800)/2, "+10")
  chart <- image_blank(width = 1920, height = 400, color = "white") |>
    image_composite(chart, offset = offset)  # 560 is the horizontal offset to center the 800px image
  
  # Create a blank image for the conclusion text
  conclusion <- image_blank(width = 1920, height = 100, color = "white") |>
    image_annotate(conclusion, size = 25, color = "black", location = "+30+20")
  
  
  #Combine text and the first image vertically
  combined <- c(heading, chart, conclusion) |>
    image_append(stack = TRUE)
  
  return(combined)
}



ele1 <- create_element("Ele 1", "../asset/image-asset2.jpeg", "Very good show this period")
ele2 <- create_element("Ele 2", "../asset/image-asset2.jpeg", "Very good show this period")

pdf_output <- c(ele1, ele2)
image_write(
  pdf_output, 
  path = paste0("reports/", "charts_with_text.pdf"), 
  format = "pdf"
)
