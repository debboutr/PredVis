library(foreign)

pb <- winProgressBar(title="progress bar", 
                     label="0% done", min=0, max=100, initial=0)

setwd("C:/Users/rdebbout/Metadata/NLCD")
rgns <- c("01","02","03S","03N","03W","04","05","06","07","08","09","10L","10U",
"11","12","13","14","15","16","17","18")

metric <- "NLCD2006_Ws"
print(metric)
# 
# VarSum <- function(df)round((sum(df$VALUE_11+df$VALUE_12+df$VALUE_21+df$VALUE_22+
#                              df$VALUE_23+df$VALUE_24+df$VALUE_31+df$VALUE_41+
#                              df$VALUE_42+df$VALUE_43+df$VALUE_52+df$VALUE_71+
#                              df$VALUE_81+df$VALUE_82+df$VALUE_90+df$VALUE_95)
#                              *0.000001),digits=4)
# UpVarSum <- function(df)round((sum(df$UpVALUE_11+df$UpVALUE_12+df$UpVALUE_21+
#                                df$UpVALUE_22+df$UpVALUE_23+df$UpVALUE_24+
#                                df$UpVALUE_31+df$UpVALUE_41+df$UpVALUE_42+
#                                df$UpVALUE_43+df$UpVALUE_52+df$UpVALUE_71+
#                                df$UpVALUE_81+df$UpVALUE_82+df$UpVALUE_90+
#                                df$UpVALUE_95)*0.000001),digits=4)
Compare <- function(df)if(df$UpCatAreaSqKM != df$UpCatVarAreaSqKM){T4 <- c(df$CatAreaSqKM,
                            df$CatVarAreaSqKM,df$UpCatAreaSqKM,df$UpCatVarAreaSqKM)}  

for (k in 3:21){
  
  table <- read.csv(paste(c("NLCD2006_Ws",rgns[10],".csv"),collapse=''))
#   #table <- read.csv("NLCD2006_Ws09.csv")
#   T1 <- ddply(table, c("COMID","UpCatAreaSqKM"),UpVarSum)
#   print(paste(c("T1_",rgns[k]),collapse=''))
#   T2 <- ddply(table, c("COMID","CatAreaSqKM"),VarSum)
#   print(paste(c("T2_",rgns[k]),collapse=''))
#   T3 <- merge(T1,T2,by.x="COMID",by.y="COMID")
#   print(paste(c("T3_",rgns[k]),collapse=''))
#   colnames(T3) <- c("COMID","UpCatAreaSqKM","UpTotVarSqKM","CatAreaSqKM",
#                     "TotVarSqKM")
  
Area <- ddply(table,"COMID",summarise,UpCatAreaSqKM=UpCatAreaSqKM,UpCatVarAreaSqKM 
            = (round((sum(UpVALUE_11+UpVALUE_12+UpVALUE_21+UpVALUE_22+UpVALUE_23+
            UpVALUE_24+UpVALUE_31+UpVALUE_41+UpVALUE_42+UpVALUE_43+UpVALUE_52+
            UpVALUE_71+UpVALUE_81+UpVALUE_82+UpVALUE_90+UpVALUE_95)*0.000001),
            digits=4)),CatAreaSqKM=CatAreaSqKM,CatVarAreaSqKM=(round((sum(VALUE_11+
            VALUE_12+VALUE_21+VALUE_22+VALUE_23+VALUE_24+VALUE_31+VALUE_41+VALUE_42+
            VALUE_43+VALUE_52+VALUE_71+VALUE_81+VALUE_82+VALUE_90+VALUE_95)
            *0.000001),digits=4)))
  print(paste(c("Area_",rgns[k]),collapse=''))
  T4 <- ddply(Area,"COMID",Compare)
  print(paste(c("T4_",rgns[k]),collapse=''))
  colnames(T4) <- c("COMID","UpCatAreaSqKM","UpTotVarSqKM","CatAreaSqKM",
                    "TotVarSqKM")

  #write.csv(T4,("C:/Users/rdebbout/Metadata/AreaOutput.csv"),row.names=F)
  write.csv(T4,paste(c("C:/Users/rdebbout/Metadata/Area/NLCD2006_WS_Area_Comp",
                     rgns[10],".csv"),collapse=""),row.names=F)
  
   info <- sprintf("%d%% done", round((k/21)*100))
   setWinProgressBar(pb, k/(21)*100, label=info)
}                     
close(pb)
