/*
 * -- Exercise 8 --
 * -- Task 1: Ranking - 10 most popular songs --
 */

// Read samples - this file has comma as separator
 val samples = spark.read.format("com.databricks.spark.csv").
  option("sep",",").
  csv("../Lab_5/samples_formatted.txt").
  toDF("user_id", "song_id", "date_timestamp", "date_id")

// Read songs file - required vertical separator as "sep"
 val songs = spark.read.format("com.databricks.spark.csv").
  option("sep","\u000b").
  csv("../Lab_5/tracks_unique.txt").
  toDF("song_id", "artist", "title")

// Group by song_id, next count elements in each group
// Join because we must know song's artist and title
// Select only required by response columns, order results and select first 10
// 'false' in show required because we should show song's title (No truncate it)
samples.groupBy("song_id").
  count().
  join(songs, "song_id").
  select("title", "artist", "count").
  orderBy(desc("count")).
  show(10, false)
