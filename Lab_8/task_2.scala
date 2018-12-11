/*
 * -- Exercise 8 --
 * -- Task 2: Ranking - 10 users with the largest number of listened unique songs --
 */

// Read samples - this file has comma as separator
 val samples = spark.read.format("com.databricks.spark.csv").
  option("sep",",").
  csv("../Lab_5/samples_formatted.txt").
  toDF("user_id", "song_id", "date_timestamp", "date_id")

// From samples select only required columns
// Make it unique and group by 'user_id', next count elements in each group
// Finally order by this count and show top 10 users without truncate IDs.
samples.select("user_id", "song_id").
  groupBy("user_id", "song_id").
  count().
  select("user_id").
  groupBy("user_id").
  count().
  orderBy(desc("count")).
  show(10, false)
