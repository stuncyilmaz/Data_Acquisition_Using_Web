# ui.R

shinyUI(fluidPage(
  sidebarLayout(
    sidebarPanel(
      p("The blue points indicate that the restaurant is closed and the orange points indicate that it is open."),
      br(),
      selectInput("var", 
                  label = "Choose a day",
                  choices = c('Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'),
                  selected = "Wednesday"),
      
      sliderInput("bins", "Time of the day (0-23):", 
                  min = 0, max = 23, value = 12, step = 1,
                  format="#.#",animate=
                    animationOptions(interval=3000, loop=TRUE))
    ),
    
    mainPanel(plotOutput("map"))
  )
))
