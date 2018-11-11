#!/bin/bash
gawk -F'<SEP>' '{
  split($4, date, "-");
  months[date[2]]++;
}
END {
  n = asorti(months, indexes);

  for (i = 1; i <= n; i++) {
    print indexes[i] " " months[indexes[i]];
  }
}' samples_formatted.txt
