/*
 * -- Exercise 8 --
 * -- Task 3: Artist with the largest number of listened songs --
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

// From samples select only song ID
// Next join song's details and group by 'artist'
// Count elements in group, order it and select only first (largest count)
samples.select("song_id").
  join(songs, "song_id").
  groupBy("artist").
  count().
  orderBy(desc("count")).
  select("artist", "count").
  show(1, false)
