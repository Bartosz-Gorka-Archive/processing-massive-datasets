#!/bin/bash
gawk -F $'\v' '{
  if ($2 == "Queen") {
    print $1 > "ex_5_1.tmp"
  }
}' tracks_unique.txt

gawk -F '<SEP>' '
FNR==NR {
  queen[$1] = $1
}
FNR!=NR {
  if ($2 in queen) {
    listen[$2]++
    print $1 " " $2 > "ex_5_2.tmp"
  }
}
END {
  for (key in listen) {
    print key " " listen[key] > "ex_5_3.tmp"
  }
}' ex_5_1.tmp samples_formatted.txt

sort --numeric-sort -k 2 -r ex_5_3.tmp | head -n 3 > ex_5_4.tmp
sort ex_5_2.tmp | uniq > ex_5_5.tmp

gawk '
FNR==NR {
  queen[$1] = $1
}
FNR!=NR {
  if ($2 in queen) {
    listen[$1]++
  }
}
END {
  for (key in listen) {
    print key " " listen[key] > "ex_5_6.tmp"
  }
}' ex_5_4.tmp ex_5_5.tmp

sort --numeric-sort -k 2 -r ex_5_6.tmp > ex_5_7.tmp

gawk '{
  if ($2 == "3") {
    print $1 > "ex_5_8.tmp"
  }
}' ex_5_7.tmp

sort ex_5_8.tmp | head -n 10

rm ex_5_1.tmp ex_5_2.tmp ex_5_3.tmp ex_5_4.tmp ex_5_5.tmp ex_5_6.tmp ex_5_7.tmp ex_5_8.tmp
