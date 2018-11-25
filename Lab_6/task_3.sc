/*
 * -- Exercise 6 --
 * -- Task 3: ApproximatePI --
 */
var n = 100000
var x = 1 to n
var iterations = 10

for (iteration <- 1 to iterations) {
  val pi_by_4 = sc.parallelize(x).map({ case(i) =>
    var x = math.random
    var y = math.random

    if(x*x + y*y <= 1) {
      ("in", 1)
    } else {
      ("out", 1)
    }
  }).reduceByKey(_ + _).collect().filter(_._1 == "in")

  println(f"$iteration%2.0f: π value is ~ " + 4.0 * pi_by_4(0)._2/n)
}
