#!/bin/bash
gawk -F',' '{
  listen[$2]++;
}
END {
  for (key in listen) {
    print key "\v" listen[key] > "ex_1_1.tmp"
  }
}' samples_formatted.txt

sort --numeric-sort -t $'\v' -k 2 -r ex_1_1.tmp | head -n 10 > ex_1_2.tmp
sort -t $'\v' -k 1 ex_1_2.tmp > ex_1_3.tmp
join -1 1 -t $'\v' ex_1_3.tmp tracks_unique.txt > ex_1_4.tmp
sort --numeric-sort -t $'\v' -k 2 -r ex_1_4.tmp > ex_1_5.tmp
gawk -F $'\v' '{
  print $4 " " $3 " " $2
}' ex_1_5.tmp
rm ex_1_1.tmp ex_1_2.tmp ex_1_3.tmp ex_1_4.tmp ex_1_5.tmp
