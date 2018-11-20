#!/bin/bash
gawk -F',' '
FNR==NR {
  dates[$1][1] = $2
  dates[$1][2] = $3
  dates[$1][3] = $4
}
FNR!=NR {
  months[dates[$4][2]]++;
}
END {
  n = asorti(months, indexes);

  for (i = 1; i <= n; i++) {
    print indexes[i] " " months[indexes[i]];
  }
}' dates.txt samples_formatted.txt
