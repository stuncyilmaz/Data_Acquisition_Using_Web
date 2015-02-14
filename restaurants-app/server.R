library(shiny)
library(ggplot2)
library(ggmap)
library(jsonlite)
library(png)
library(grid)
library(RCurl)
library(plyr)
library(markdown)

source("restaurant_helpers.R")
library("ggplot2")
library("ggmap")

restaurants=data.frame()
files=c("data/operating_hours_Mon.csv","data/operating_hours_Tue.csv",
        "data/operating_hours_Wed.csv","data/operating_hours_Thu.csv",
        "data/operating_hours_Fri.csv","data/operating_hours_Sat.csv",
        "data/operating_hours_Sun.csv")
days=c('Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday')

for(i in seq(1:7)) {
#rbind other days as well
restaurants_dummy=read.csv(files[i],header=TRUE)
restaurants_dummy$opening_1_hours=sapply(restaurants_dummy[,c('opening_1')], function(x) getHour(x) )
restaurants_dummy$closing_1_hours=sapply(restaurants_dummy[,c('closing_1')], function(x) getHour(x) )
restaurants_dummy$day=days[i]
if (i==0){restaurants=rbind(restaurants_dummy)}
else {restaurants=rbind(restaurants,restaurants_dummy)}
}
restaurants=subset(restaurants, ! (is.na( closing_1_hours) | is.na(opening_1_hours)))
restaurants=subset(restaurants, ! (is.na( latitude) | is.na(longitude)))

gmap <- ggmap(get_map(location=c(lon=-122.425,lat=37.78),zoom=13,maptype='roadmap',scale=2,source='google',color='bw'), 
                extent = "device", fullpage = T)

shinyServer(
  function(input, output) {
    output$map <- renderPlot({
      
      
      myday <- switch(input$var, 
                      "Monday" = "Monday",
                      "Tuesday" = "Tuesday",
                      "Wednesday" ="Wednesday",
                      "Thursday" = "Thursday",
                      "Friday" = "Friday",
                      "Saturday" = "Saturday" ,
                      "Sunday" = "Sunday"
          
      )
      data <-restaurants[restaurants$day==myday,]
      
      p=reactive({plotfunc(data,input$bins,myday)})
      print(gmap+p()[1]+p()[2])
    },height=650)
  }
)
