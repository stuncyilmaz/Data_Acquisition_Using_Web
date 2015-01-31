# ui.R

shinyUI(fluidPage(
  titlePanel("SF Restaurants"),
  h1(""),
  #p("Shiny is a new package from RStudio that makes it ", 
    #em("incredibly easy"), 
    #" to build interactive web applications with R."),
  br(),
  p("Our application uses Shiny to visualize the operating hours of a random sample of restaurants in San Francisco for each day of the week. 
    For the source code of our project, visit the ",
    a("GitHub Homepage.", 
      href = "https://github.com/SandeepReddyVanga/Data_Acquisition_Using_Web")),
  br(),
  h2("Introduction"),
  br(),
  p("We are TravelWorldSpunky, a group formed by three Data Science students in the city of San Francisco. We want make a trip memorable and hassle free by providing local information & recommending local events to travelers in real time. To start with, also being food-lovers, we want to create a better solution to help people like us locate food no matter where and when they are in San Francisco."),
  #p("* Shiny applications are automatically “live” in the same way that ", 
    #strong("spreadsheets"),
    #" are live. Outputs change instantly as users modify inputs, without requiring a reload of the browser."),
  br(),
  h2("User Guide"),
  br(),
  p("It is very simple to play with this application. You just need to: "),
  p("* Select the day of the week from the drop-down menu"),
  p("* Click on the start button to begin and click again to pause"),
  br(),
  h2("Features"),
  p("The blue points indicate the restaurants that are closed and the orange points indicate the restaurants that are open."),
  br(),
  h2("Installation"),
  p("Shiny is available on CRAN, so you can install it in the usual way from your R console:"), code('install.packages("shiny")'),
  br(),

  sidebarLayout(
    sidebarPanel(
      br(),
      br(),
      #h2("Installation"),
      #p("Shiny is available on CRAN, so you can install it in the usual way from your R console:"),
      #code('install.packages("shiny")'),
      #br(),
      #br(),
      #br(),
      #br(),
      #img(src = "bigorb.png", height = 72, width = 72),
      #"shiny is a product of ", 
      #span("RStudio", style = "color:blue"),
      #helpText("Create demographic maps with 
        #information from the 2010 US Census."),
      #br(),
      #br(),
      selectInput("var", 
                  label = "Choose A Day",
                  choices = c('Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'),
                  selected = "Wednesday"),
      
      # try to understand 
      sliderInput("bins", "Time of the day (0-23):", 
                  min = 0, max = 23, value = 12, step = 1,
                  format="#.#",animate=
                    animationOptions(interval=3000, loop=TRUE))
     
    ),
    # plotOutput is a built-in function 
    mainPanel(plotOutput("map"))
  )
))