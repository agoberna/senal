import re
import sys

with open(sys.argv[1], 'r') as ifile:
    text = ifile.read()
ifile.close()

clean_regex = re.compile('<.*?>')
cleantext = re.sub(clean_regex, '  ', ''.join(text))
cleantext2 = re.sub(' +', ' ', cleantext)

print(cleantext2)
