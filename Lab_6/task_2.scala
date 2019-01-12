/*
 * -- Exercise 6 --
 * -- Task 2: MatrixVectorMultiplication --
 */
val vector = sc.textFile("files/x.txt").map(line => {
  val value = line.split(",")
  value(1).trim.toDouble
}).collect()
val broadcasted = sc.broadcast(vector)

val matrix = sc.textFile("files/M.txt").map(line => {
  val value = line.split(",")
  (value(0).trim.toInt, value(1).trim.toInt, value(2).trim.toDouble)
})

val result = matrix.map({case(i, j, v) => (i, v * broadcasted.value(j - 1))}).reduceByKey(_ + _)
result.sortBy(_._1).toDF.show
