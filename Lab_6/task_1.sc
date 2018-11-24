/*
 * -- Exercise 6 --
 * -- Task 1: WordCount --
 */
val source = sc.textFile("files/all-shakespeare.txt")
val counts = (source.flatMap(line => line.split("\\s+"))
              .map(word => (word, 1))
              .reduceByKey(_ + _)
              .sortBy(- _._2))

counts.saveAsTextFile("task_1")
