# import re
#
# def find_invalid_characters(input_string, pattern):
#     # Используем re.findall() для поиска всех совпадений
#     invalid_characters = re.findall(f'[^{pattern}]', input_string)
#     return invalid_characters
#
# # Пример использования:
# user_input = "Hello_World123@#$"
# allowed_pattern = r'[a-zA-Z_]'  # Паттерн для разрешенных символов (буквы и подчеркивание)
# invalid_chars = find_invalid_characters(user_input, allowed_pattern)
#
# if invalid_chars:
#     print(f"Недопустимые символы: {', '.join(invalid_chars)}")
# else:
#     print("Все символы соответствуют паттерну.")

# import re
#
# USERNAME_PATTERN = r'^[A-Za-z0-9]+$'
# text = 'Uladzimir Lasouski +'
# # нет групп захвата
# match = re.findall(USERNAME_PATTERN, text)
# print(match)
#
# import re
#
# text = "Python is an amazing programming language. Python is widely used."
# pattern = r'^[A-Za-z0-9]+$'
#
# matches = re.findall(pattern, text)
# print("Совпадений найдено:", len(matches))


import re
#
#
# def check_alphanumeric(input_string):
#     # Регулярное выражение для поиска символов, состоящих только из букв и цифр
#     pattern = r"[A-Za-z0-9]"
#     # pattern = f'[^{pattern}]'
#     result = re.findall(pattern, input_string)
#     result_1 = ''.join(result)
#     # Проверяем, соответствует ли строка регулярному выражению
#     if result:
#         print(f"Строка '{input_string}' состоит только из букв и цифр.")
#         print(result)
#         print(result_1)
#         print(set(input_string) - set(result_1))
#     else:
#         print(f"Строка '{input_string}' содержит недопустимые символы.")
#         print(result)
#         print(result_1)
#
#
#
#
# # Пример использования
# user_input = "Pyth on"
# check_alphanumeric(user_input)


USERNAME_PATTERN = r'^[\w.@+-]+\Z'
CHAR_PATTERN = r'[\w.@+-]'
username = "Ula d+"
if re.findall(USERNAME_PATTERN, username):
    print('DA')
else:
    print(re.findall(CHAR_PATTERN, username))
    difference = set(username) - set(re.findall(CHAR_PATTERN, username))
    print(difference)


# if re.findall(USERNAME_PATTERN, username) == [username]:
#     pass
# else:
#     result_set = (re.findall(USERNAME_PATTERN, char) for char in username)
#
# difference = (set(username) - set(re.findall(USERNAME_PATTERN, username)))
# print(difference)