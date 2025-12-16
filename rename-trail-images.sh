#!/bin/bash

# Rename trail figure images (working backwards to avoid conflicts)
cd img
for old_num in 22 21 20 19 18 17 16 15 14 13; do
  new_num=$((old_num + 1))
  for f in trail-${old_num}-figure-*; do
    if [ -f "$f" ]; then
      new_f=$(echo "$f" | sed "s/trail-${old_num}-/trail-${new_num}-/")
      mv "$f" "$new_f" && echo "Renamed $f -> $new_f"
    fi
  done
done
cd ..
