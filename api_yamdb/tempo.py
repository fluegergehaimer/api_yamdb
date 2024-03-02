import re

pattern = r'^[\w.@+-]+\Z'
pattern_1 = r'[\w.@+-]+'
username = 'Bor&is14@%'

results = re.finditer(pattern, username)
results_1 = re.findall(pattern_1, username)

print('results:')
for i in results:
    print(i)

print('results_1:', results_1)

split_string = re.split(pattern, username)
print(split_string)