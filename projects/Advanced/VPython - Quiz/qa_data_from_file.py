import re

'''
Pleake keep the following in mind while adding to the data.txt

1. Do not use '?'.
2. Do not directly copy and paste the quotes from the internet.Those special ones won't work.
Replace them with the normal ones like " '.
'''


def main(file_name):
    with open(file_name, encoding='utf-8') as file:
        data_str = file.read()
    regex_question, regex_answer = generate_regex(file_name)
    questions = regex_question.findall(data_str)
    answers = regex_answer.findall(data_str)
    q_and_a = zip(questions, answers)
    return q_and_a


def generate_regex(file_name):
    if file_name in ['Etymology.txt']:
        regex_question = re.compile(r"W\.[\w',()\s]*\|")
        regex_answer = re.compile(
            r"\|[a-zA-Z0-9.\:,='\"\s\-\+\-()\[\];\*>!_{}@&#\/\\]*W\.")
        return regex_question, regex_answer

    elif file_name in ['Data.txt', 'Pandas_data.txt']:
        regex_question = re.compile(r'\bQ.*\?')
        regex_answer = re.compile(
            r"\bA\.[a-zA-Z0-9.\:,='\"\s\-\+\-()\[\];\*><!_|{}@&#\/\\]*\.\.")
        return regex_question, regex_answer


# result = main('Pandas_data.txt')
# counter = 0
# for item in result:
#     print(item[0][2:])
#     print(item[1][2:-2])
#     counter += 1
#     print("--------------------------------------")
# print(counter)


# \bA\.[a-zA-Z0-9.\:,='\"\s\-\+\-()\[\];\*>!_|{}@#\/\\]*\.\. == here we are just looking for all the possible characters between
# A. and ..all those possible ones are included in the brackets part - []*, But stranges, some of them are working even
# though they are not escaped. like . () etc., .
