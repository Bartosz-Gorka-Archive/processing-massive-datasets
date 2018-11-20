#!/bin/bash
gawk -F',' '{
  listen[$2]++;
}
END {
  for (key in listen) {
    print key "\v" listen[key] > "ex_3_1.tmp"
  }
}' samples_formatted.txt

sort -t $'\v' -k 1 ex_3_1.tmp > ex_3_2.tmp
join -1 1 -t $'\v' ex_3_2.tmp tracks_unique.txt > ex_3_3.tmp

gawk -F $'\v' '{
  listen[$3] += $2;
}
END {
  for (key in listen) {
    print key "\v" listen[key] > "ex_3_4.tmp"
  }
}' ex_3_3.tmp

sort --numeric-sort -t $'\v' -k 2 -r ex_3_4.tmp > ex_3_5.tmp
head -n 1 ex_3_5.tmp > ex_3_6.tmp
gawk -F $'\v' '{
  print $1 " " $2
}' ex_3_6.tmp

rm ex_3_1.tmp ex_3_2.tmp ex_3_3.tmp ex_3_4.tmp ex_3_5.tmp ex_3_6.tmp
