#!/usr/bin/python

with open(FileName) as f:
  newText=f.read().replace('A', 'Orange')

with open(FileName, "w") as f:
  f.write(newText)
