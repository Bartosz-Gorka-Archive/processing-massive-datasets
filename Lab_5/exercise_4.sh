#!/bin/bash
gawk -F'<SEP>' '{
  split($4, date, "-");
  months[date[2]]++;
  print $0 " | " date[2] " | " months[date[2]] > "testowe.txt"
}
END {
  n = asorti(months, indexes);

  for (i = 1; i <= n; i++) {
    print indexes[i] " " months[indexes[i]];
  }
}' samples_formatted.txt
