/*
 * -- Exercise 8 --
 * -- Task 4: Listened songs' count per each month --
 */

// Read samples and dates - these files have comma as separator
 val samples = spark.read.format("com.databricks.spark.csv").
  option("sep",",").
  csv("../Lab_5/samples_formatted.txt").
  toDF("user_id", "song_id", "date_timestamp", "date_id")
val dates = spark.read.format("com.databricks.spark.csv").
  option("sep",",").
  csv("../Lab_5/dates.txt").
  toDF("date_id","year","month","day")

samples.select("date_id").
  join(dates, samples("date_id") === dates("date_id")).
  groupBy("month").
  count().
  orderBy(asc("month")).
  select("month", "count").
  show(false)
