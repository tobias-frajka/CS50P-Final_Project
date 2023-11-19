# Password Generator and Security Checker
#### Video Demo:  https://www.youtube.com/watch?v=QM1ZuTNu2Mo

## Introduction

This Python program is a versatile **Password Generator and Security Checker** developed by Tobias Frajka as a final project for CS50P. It allows users to generate secure passwords based on their specified criteria and check the security of generated passwords by querying the "Have I Been Pwned" (HIBP) API to see if they have been involved in data breaches. This tool is designed to help users create strong, unique passwords for various online accounts and services.

## Features

- **Password Generation**: The program generates random passwords with customizable attributes such as length, character types (digits, letters, special characters), and exact requirements for uppercase letters, digits, and special characters.

- **Security Checking**: It checks the generated passwords against the HIBP API to determine if they have appeared in any known data breaches. If a breach is detected, the program tries to generate a new password for increased security.

- **Customization**: Users can specify the length of the password and the desired character types, making it suitable for various password policies and requirements.

- **File Saving**: Optionally, users can choose to save multiple generated passwords to a file named `passwords.txt`, making it convenient to store and manage multiple passwords.

- **Error Handling**: The program handles various error scenarios gracefully, including incorrect input parameters and API request errors.

## How to Use

1. **Installation**: Ensure you have Python installed on your system.

2. **Command-Line Usage**: Run the program from the command line with the following options:

    `python password_generator.py length -t {0, 1, 2, 3} [options]`

- `length`: Specify the length of the password. Minimum is 1 character and maximum is 100. (Required)
- `-t` or `--type`: Specify the password type (0 for digits, 1 for letters, 2 for digits and letters, 3 for digits, letters, and special characters). (Required)
- `-s` or `--save`: Specify the number of passwords to generate and save to a file. (Optional)
- `-u` or `--uppercase`: Specify the exact number of uppercase letters in the password. (Optional)
- `-n` or `--numbers`: Specify the exact number of digits in the password. (Optional)
- `-c` or `--characters`: Specify the exact number of special characters in the password. (Optional)
- `-h` or `--help`: How to use in terminal

3. **Generated Passwords**: The program will generate passwords based on your criteria and display them in the terminal. If a password has been involved in data breaches, it will try to generate a new one.

4. **File Saving (Optional)**: If you used the `-s` option, the generated passwords will also be saved to a file named `passwords.txt`.

## Security Considerations

- **Length**: Ensure that you select an appropriate password length based on your specific security requirements. Longer passwords are generally more secure.

- **Character Types**: Consider including a mix of character types (uppercase letters, digits, special characters) in your passwords for enhanced security.

- **Data Breach Checking**: Be aware that the program relies on the HIBP API to check for data breaches. While this is a valuable tool, it's essential to use strong, unique passwords for critical accounts and enable multi-factor authentication when available.

## Design choices

Project started with fairly limited scope and focused on basic functionality (generating safe passwords) at the beginning, with more advanced functions coming later in the development cycle. I wasn't entirely sure if the password should be it's own class, but later chose not to do it as a object, because of only one instance and a lot of unnecessary difficulty in implementing it. I really enjoyed working with `argparse`, which really helped me speed up the development because of not having to make my own tool to parse arguments or using `sys.argv`.

## Tests

Included in the project are unit tests built for testing functions inside the `project.py` file for PyTest. You can run them with the:

`pytest test_project.py`

This file consists of several functions aimed at testing proper functionality of functions inside of main file. Based on these tests, there were made some changes to the structure of the main file because of using `argparse`, tool for parsing command-line arguments.

## Acknowledgments

This program utilizes the "Have I Been Pwned" API to check for data breaches. Credit and thanks to the HIBP team for providing this service.

