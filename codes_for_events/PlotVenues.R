
rm(list=ls())
setwd("/home/tunc/Desktop/Data_aqcuisition/Project")
#install.packages("ggmap")
library("ggplot2")
library("ggmap")
#install.packages("directlabels")
library(directlabels)
require(RColorBrewer, quietly = T)

filename="venueExamples.csv"
df <- read.csv(filename, sep=",", header=TRUE )

filename="query3.csv"
df2a <- read.csv(filename, sep=",", header=FALSE )

names(df2a)=c("venue_name","latitude","longitude","weight", "bus_name", "bus_latitude","bus_longitude" )
df2= df2a[sample(1:nrow(df2a), 10,replace=FALSE),]




#maptype = c("terrain", "satellite", "roadmap", "hybrid", "toner", "watercolor")
map1<-get_map(location=c(lon=-122.43,lon=37.76),zoom=12,maptype='roadmap',source='google',color="bw")
p<-ggmap(map1)

colors <- brewer.pal(10, "Paired") 

p=p+geom_point(aes(x=longitude, y=latitude,size = weight,color = venue_name),  # Points are added and color cooded according to "Type"
               data = df2, alpha = 0.5, position = "jitter")+scale_size(range = c(2, 20), name="weights")+
  scale_color_manual(values = colors) 
p=p+geom_point(aes(x=bus_longitude, y=bus_latitude),  # Points are added and color cooded according to "Type"
               data = df2, alpha = 0.5, position = "jitter",size = 4,color = "black",shape=25,fill="black")