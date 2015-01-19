# GIFs of the Operating Hours 

gif_operating_hours_generation <- function(filename) {

  data <- read.csv(filename,header=TRUE)
  open <- as.data.frame(data$opening_1_hours)[,1]
  close <- as.data.frame(data$closing_1_hours)[,1]
  combined <- c(open,close)
  time <- sort(unique(combined))

  plotfunc <- function(x) {
    cols <- c("Closed"="deepskyblue2","Open" = "orange")
    df <- subset(data, opening_1_hours<= x & closing_1_hours> x)
    df_1 <- subset(data, opening_1_hours> x | closing_1_hours<= x)
    df$lan <- as.numeric(df$latitude)
    df$lon <- as.numeric(df$longitude)
    p <- ggmap(get_map(location = c(lon = -122.41,lon = 37.78), zoom = 12, maptype = "roadmap", source = "google", color = "bw")) +
          geom_point(data = df, aes(x = longitude, y = latitude), colour = "orange", alpha = 0.8, size = 5)  + 
          geom_point(data = df_1, aes(x = longitude, y = latitude), colour = "deepskyblue2", alpha = 0.8, size = 3, position = "jitter")
    }

#get them into a different color 

  saveGIF(
  {
    for (i in time) print(plotfunc(i))
  },
  movie.name = paste(filename,".gif",sep=""), img.name = "Rplot",convert = "convert",
  interval = 0.8, 
  ani.width = 1200, 
  ani.height = 1200
  )

}


# take Wednesday as an example 

gif_operating_hours_generation("operating_hours_Wed.csv")






# ggmap of the Restaurant Categories 

cate <- read.csv("category.csv", header = T)
categories <- sort(unique(cate$category))
Asian <- c("Chinese", "Japanese", "Korean", "Vietnamese", "Thai", "Indian", "Singaporean", "Laotian", "Filipino", "Hawaiian", "Afghan", "Asian Fusion", "Burmese")
Mediterranean <- c("Turkish", "Mediterranean")
Middle_Eastern <- c("Middle Eastern")
European <- c("French", "Czech", "Moroccan", "Italian", "Spanish", "British")
African <- c("Ethiopian", "South African")
Mexican <- c("Peruvian", "Latin American", "Mexican","Argentine")
American <- c("American (New)", "American (Traditional)")
clutter <- c(Asian,Mediterranean,Middle_Eastern,European,African,Mexican,American)
indices <- sort(match(clutter,categories))
Others <- categories[-indices]

cate$group <- with(cate, ifelse(category %in% Asian, "Asian",
                            ifelse(category %in% Mediterranean, "Mediterranean", 
                                     ifelse(category %in% Middle_Eastern, "Middle Eastern",
                                            ifelse(category %in% European, "European",
                                                   ifelse(category %in% African, "African",
                                                          ifelse(category %in% Mexican, "Mexican",
                                                                 ifelse(category %in% American, "American", "Others"))))))))
#palette(rainbow(8))     # six color rainbow

p <- ggmap(get_map(location = c(lon = -122.41,lon = 37.78), zoom = 12, maptype = "roadmap", source = "google", color = "bw"))
p <- p + geom_point(data = cate, aes(x = longitude, y = latitude, color = group), size = 3, position = "jitter")
p <- p + scale_color_brewer(palette = "Set1")
p <- p + labs(title = "SF Map of Restaurants by Categories")
p <- p + xlab("Longitude")
p <- p + ylab("Latitude")
p 
ggsave("SF Map of Restaurants by Categories.png")






                                                                
                                        



