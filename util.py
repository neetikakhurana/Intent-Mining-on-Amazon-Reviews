import re

# useful for stripping apostrophe's in a word    
def quoterepl(matchobj):
  return matchobj.group(0).replace('\'', '')

# useful in convering single to double quotes required by the JSON module
def dataCleanup(line):
  # replace any single quotes in the text with nothing as these will be
  # removed during tokenization anyway
  line = re.sub('[a-zA-Z]+\'[a-zA-Z]+', quoterepl, line)

  # product data for some reason had single quotes for all keys which is
  # not allowed by json.loads() so had to replace with a double quote 
  line = line.replace('\'', '\"')

  return line
