import gzip
import json


def parse(filename):
  f = gzip.open(filename, 'rt')
  for l in f:
    l = l.strip()
    yield l

def dataInJson(line):
  dij = None
  try:
    dij = json.loads(line)
  except ValueError:
    pass

  return dij


  
