
plotfunc <- function(data,mytime,myday,gmap) {
  cols <- c("Closed"="deepskyblue2","Open"="orange")
  data=subset(data, day==myday)
  # when opening time < closing time
  
  data_dummy=subset(data, (opening_1_hours<closing_1_hours))
  df_a <- subset(data_dummy, (opening_1_hours<= mytime & closing_1_hours> mytime))
  df_1_a<-subset(data_dummy, !(opening_1_hours<= mytime & closing_1_hours> mytime))
  
  # when opening time > closing time
  data_dummy=subset(data, (opening_1_hours>=closing_1_hours))
  df_1_b <- subset(data_dummy, (closing_1_hours<= mytime & opening_1_hours> mytime))
  df_b<-subset(data_dummy, !(closing_1_hours<= mytime & opening_1_hours> mytime))
  
  
  df=rbind(df_a,df_b)
  df_1=rbind(df_1_a,df_1_b)
  
  
  p <- gmap+
    geom_point(data=df,aes(x=longitude,y=latitude),colour = 'orange',alpha=0.8,size=3)+
    	geom_point(data=df_1,aes(x=longitude,y=latitude),colour='deepskyblue2',alpha=0.8,size=3,position = "jitter")
  p
}


getHour <- function(x){
  
  if (x=='0:00 am'){return(0)}
  if (x=='0:00 pm'){return(12)}
  
  my_time= strptime(x, "%I:%M %p")
  my_hour=as.numeric(strftime(my_time, format="%H"))+as.numeric(strftime(my_time, format="%M"))/60
  my_hour
}