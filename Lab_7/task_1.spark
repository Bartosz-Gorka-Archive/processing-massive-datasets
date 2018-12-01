/*
 * -- Exercise 7 --
 * -- Task 1: Aggregation --
 */

// Import required Random and generate records
import scala.util.Random
val groups = Map(
  0 -> (0, 1),
  1 -> (1, 1),
  2 -> (2, 2),
  3 -> (3, 3),
  4 -> (4, 3),
  5 -> (5, 2),
  6 -> (6, 1)
)
val n = 1000000
val random = Random
val data = sc.parallelize(
  for (i <- 1 to n) yield {
    val g = random.nextInt(7)
    val (mu,sigma) = groups(g)

    (g, mu + sigma * random.nextGaussian())
  }
)

// Make groups in format (GROUP_ID, (Count, Value, Value^2))
val records = (data
  .map(t => (t._1, (1, t._2, t._2 * t._2)))
  .reduceByKey((a, b) => (a._1 + b._1, a._2 + b._2, a._3 + b._3))
)

// Cache it to speed up calculations
records.cache()

// Aggregate in format (Group ID, (Sum count this group in all records, Average value, Variance))
val groups_aggregated_stats = records.map(r => (r._1, (r._2._1, r._2._2 / r._2._1, ((r._2._3 - ((r._2._2 * r._2._2) / r._2._1)) / r._2._1))))
// Print in new line each group stats
groups_aggregated_stats.collect().foreach(println)

// Aggregate results in all groups to single group "all records"
val all_records_stats = records.reduce((a, b) => (0, (a._2._1 + b._2._1, a._2._2 + b._2._2, a._2._3 + b._2._3)))
val results = (all_records_stats._2._1, all_records_stats._2._2 / all_records_stats._2._1, ((all_records_stats._2._3 - ((all_records_stats._2._2 * all_records_stats._2._2) / all_records_stats._2._1)) / all_records_stats._2._1))

// Return result as (Total count, Total average, Total variance)
println(results)
