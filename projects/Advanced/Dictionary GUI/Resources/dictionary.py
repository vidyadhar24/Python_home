# A simple dictionary application

import requests
from pathlib import Path
import sys
import os


def main():

    print("________________________________________________")
    print('Welcome to smart dictionary(not so much)')
    print('It allows the users to find the meaning of a word from typing in terminal \n or by giving a path of the file that contains the words.')
    print("________________________________________________")
    while True:
        dictionary_mode = input("type or file?: ").lower()
        if dictionary_mode == 'type':
            input_word = input("enter the word: ").lower()
            print()
            if input_word == 'q':
                print("Thanks for trying the application")
                sys.exit()

            try:

                headers = {
                    'Authorization': 'Token ' + open('key.txt', 'r').read(),
                }

                response = requests.get(
                    'https://owlbot.info/api/v4/dictionary/' + input_word, headers=headers)

                # directly loads the response to a dictionary object in python
                result_dict = response.json()

                # print(result_dict.keys())

                if len(result_dict) > 1:
                    for item in range(len(result_dict['definitions'])):
                        print("Type : " +
                              result_dict['definitions'][item]["type"])
                        print("Meaning : " +
                              result_dict['definitions'][item]["definition"])
                        if result_dict['definitions'][item]["example"]:

                            print("Example : " +
                                  result_dict['definitions'][item]["example"])
                        print(
                            "-----------------------------------------------------------------------------")
                else:
                    print('typo or the word is not covered.')
                    print()

            except requests.exceptions.ConnectionError:
                print('Not connected to Internet!!')

        elif dictionary_mode == 'file':
            print("Please note there is one word per one line in the file")
            file_path = input('Enter the file path: ')
            path = Path(file_path)
            file_name = os.path.basename(path).split(".")[0]
            if not path.exists():
                print("the path doesn't exist, Check again!")
            else:

                with open(file_path) as file:
                    words = file.read().split('\n')
                try:
                    headers = {'Authorization': 'Token ' +
                               open('key.txt', 'r').read(), }

                    for word in words:
                        response = requests.get(
                            'https://owlbot.info/api/v4/dictionary/' + word, headers=headers)
                        result_dict = response.json()
                        if len(result_dict) > 1:
                            new_file = file_name + "_meanings.txt"
                            with open(new_file, 'a') as file:
                                for item in range(len(result_dict['definitions'])):
                                    file.write("Word : " +
                                               result_dict["word"] + "\n")
                                    file.write("Type : " +
                                               result_dict['definitions'][item]["type"] + "\n")
                                    file.write("Meaning : " +
                                               result_dict['definitions'][item]["definition"] + "\n")
                                    if result_dict['definitions'][item]["example"]:
                                        file.write("Example : " +
                                                   result_dict['definitions'][item]["example"] + "\n")
                                    file.write(
                                        "-------------------------------------------------------------------------------" + "\n")
                                print("Definitions for", word,
                                      "saved to ", new_file)
                        else:
                            print("unable to get the meaning for " + word)
                            # print('typo or the word is not covered.')
                except requests.exceptions.ConnectionError:
                    print('Not connected to Internet!!')
        elif dictionary_mode == 'q':
            print("Thanks for trying the application")
            sys.exit()

        else:
            print("Please choose from the available options!! or 'q' to quit")


if __name__ == '__main__':
    main()
