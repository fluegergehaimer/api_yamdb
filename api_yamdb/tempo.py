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
# for i in results_1:
#     print(i)

split_string = re.split(pattern, username)
print(split_string)

# results = re.finditer (r'мыла', 'Мама мыла раму, а потом ещё раз мыла, потому что не домыла')
# print (results)
#
# for match in results:
#     print (match)
