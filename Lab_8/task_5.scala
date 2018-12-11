/*
 * -- Exercise 8 --
 * -- Task 5: 10 users who listened all 3 most popular songs prepared by Queen --
 */

// Read samples and dates - these files have comma as separator
val samples = spark.read.format("com.databricks.spark.csv").
  option("sep",",").
  csv("../Lab_5/samples_formatted.txt").
  toDF("user_id", "song_id", "date_timestamp", "date_id")
// Read songs file - required vertical separator as "sep"
val songs = spark.read.format("com.databricks.spark.csv").
  option("sep","\u000b").
  csv("../Lab_5/tracks_unique.txt").
  toDF("song_id", "artist", "title")

val top_listened_queen_songs = samples.groupBy("song_id").
  count().
  join(songs, "song_id").
  filter(col("artist") === "Queen").
  orderBy(desc("count")).
  select("title", "song_id").
  limit(3)

samples.select("song_id", "user_id").
  join(top_listened_queen_songs, "song_id").
  filter(not(col("title").isNull)).
  groupBy("user_id", "song_id").
  count().
  select("user_id").
  groupBy("user_id").
  count().
  filter(col("count") === 3).
  orderBy(asc("user_id")).
  select("user_id").
  show(10, false)
