require(rjson)

file = "nyc-zip-code.json"
nyc_zipcode = fromJSON(file=file, method = 'C')

head(nyc_zipcode)
View(nyc_zipcode)
test = nyc_zipcode[[2]][[1]][3]

View(test)

restaurant <- read.csv("restaurants_cleancuisine.csv")
head(restaurant)
cuisine_names = levels(restaurant$cuisine.type)
cuisine_names[17]
restaurant = na.omit(restaurant)
class(restaurant$rating)
class(restaurant$price)
class(restaurant$score)

library(sqldf)
if (file.exists("restaurants.sqlite") == TRUE) file.remove("restaurants.sqlite")
db <- dbConnect(SQLite(), dbname="restaurants.sqlite")
dbWriteTable(conn = db, name = 'nyc_restaurants', value = restaurant, row.names = FALSE)

total_restaurants = sqldf("Select zipcode, count(*) as num_of_restaurants, avg(rating) as rating, avg(price) as price, avg(score) as score from nyc_restaurants group by zipcode", dbname = "restaurants.sqlite")

colName = total_restaurants$zipcode
temp = data.frame(t(total_restaurants[,-1]))
colnames(temp) = colName

set.seed(1)
name = "total.json"
sink(name)
cat(toJSON(temp))
sink()

count_jewish = sqldf("Select zipcode, count(*) from nyc_restaurants where cuisine_type = 'Jewish/Kosher' group by zipcode" , dbname = "restaurants.sqlite")

len = length(cuisine_names)
range = c(1:len)
range = range[-17]

for (i in range){

cuisine = cuisine_names[i]
# cuisine = cuisine_names[17]

temp_data = sqldf(paste("Select zipcode, count(*) as num_of_restaurants, avg(rating) as rating, avg(price) as price, avg(score) as score from nyc_restaurants where cuisine_type = \'",cuisine, "\' group by zipcode", sep="") , dbname = "restaurants.sqlite")
colName = temp_data$zipcode
temp = data.frame(t(temp_data[,-1]))
colnames(temp) = colName

set.seed(1)
# name = "Jewish_Kosher.json"
name = paste(cuisine,".json",sep="")
sink(name)
cat(toJSON(temp))
sink()
}

sort(total_restaurants$num_of_restaurants)