# Author: Tobias Frajka, Password generator for final project in CS50P
import secrets, sys, argparse, string, random, hashlib, requests

MAX_PASSWORD_ATTEMPTS = 10


def main():
    """
    Generate and check passwords based on user-defined parameters.

    Parses command-line arguments, generates passwords, checks their security,
    and provides feedback to the user.
    """
    args = parse_arguments(sys.argv[1:])

    subset = get_subset(args.type)

    # If the user wants to save passwords to a file, generate and save them
    if args.save:
        generate_passwords_to_file(args.save, args, subset)
        exit()

    # Generate and check passwords for security
    for i in range(MAX_PASSWORD_ATTEMPTS):
        if args.uppercase or args.characters or args.numbers:
            requirements = {
                "uppercase": args.uppercase,
                "numbers": args.numbers,
                "characters": args.characters,
            }
            password = generate_special_password(args.length, requirements, subset)

        else:
            password = generate_password(args.length, subset)

        print(password)

        # Check if the password has been involved in data breaches
        breach_count = check_password_breach(password)

        if breach_count == -1:
            exit("API request Error")

        if breach_count > 0:
            print(
                f"This password has been involved in {breach_count} data breaches. It is not secure. Generating new password, attempt n.{i + 1}"
            )
        else:
            print(
                "This password has not been involved in any known data breaches. It appears to be secure."
            )
            exit()

    print(
        "Not able to generate secure password using set parameters, consider changing length or type of the password"
    )


def get_subset(type):
    """
    Determine the character subset based on the selected password type.

    Args:
        type (int): The selected password type (0, 1, 2, or 3).

    Returns:
        str: The character subset based on the selected type.

    Raises:
        ValueError: If the provided password type is invalid.
    """
    match type:
        case 0:
            subset = string.digits
        case 1:
            subset = string.ascii_letters
        case 2:
            subset = string.digits + string.ascii_letters
        case 3:
            subset = string.digits + string.ascii_letters + string.punctuation
        case _:
            raise ValueError("Wrong or no password type")

    return subset


def parse_arguments(arg):
    """
    Parse command-line arguments and validate user input.

    Args:
        arg (list): A list of command-line arguments.

    Returns:
        argparse.Namespace: An object containing parsed arguments.
    """
    parser = argparse.ArgumentParser(
        description="Generate a random password based on entered length and type. Maximal length is 100 characters.\
        It checks generated password (not present if saving files - '-s' is present) in databases of data breaches at 'Have I been pwned' and if found, generates new password (max. 10 attempts)"
    )

    parser.add_argument(
        "length",
        help="Length of a generated password",
        type=int,
    )

    parser.add_argument(
        "-t",
        "--type",
        help="Type of a generated password: 0 - only digits 1 - only letters 2 - digits and letters 3 - digits, letters and special characters",
        type=int,
        choices=[0, 1, 2, 3],
        required=True,
    )

    parser.add_argument(
        "-s",
        "--save",
        help="Generate s passwords with specified parameters and save them to a file named passwords.txt",
        type=int,
    )

    parser.add_argument("-u", "--uppercase", help="Exact number of uppercase letters", type=int)

    parser.add_argument("-n", "--numbers", help="Exact number of digits", type=int)

    parser.add_argument("-c", "--characters", help="Exact number of special characters", type=int)

    args = parser.parse_args(arg)

    try:
        if args.length > 100 or args.length < 0:
            sys.exit("Wrong length")

        if args.uppercase and args.type == 0:
            sys.exit("Wrong parameters")

        if args.numbers and args.type == 1:
            sys.exit("Wrong parameters")

        if args.characters and args.type != 3:
            sys.exit("Wrong parameters")

        if args.save and (args.save <= 0):
            sys.exit("Wrong parameters")

        if (
            (args.uppercase and args.uppercase > args.length)
            or (args.numbers and args.numbers > args.length)
            or (args.characters and args.characters > args.length)
            or (args.uppercase or 0) + (args.numbers or 0) + (args.characters or 0)
            > args.length
        ):
            sys.exit("Wrong parameters")

    except TypeError:
        pass

    return args


def generate_password(length, subset):
    """
    Generate a random password with the specified length and character subset.

    Args:
        length (int): The length of the password to generate.
        subset (str): The character subset to use for password generation.

    Returns:
        str: The generated password.
    """
    password = "".join(secrets.choice(subset) for i in range(length))
    return password


def generate_special_password(length, requirements, subset):
    """
    Generate a password with specific requirements (uppercase, numbers, special characters).

    Args:
        length (int): The length of the password to generate.
        requirements (dict): A dictionary specifying the requirements for the password.
            - uppercase (int): Exact number of uppercase letters.
            - numbers (int): Exact number of digits.
            - characters (int): Exact number of special characters.
        subset (str): The character subset to use for password generation.

    Returns:
        str: The generated password.
    """
    random.seed(secrets.randbelow(10000000000))

    temp_len = length

    password = ""

    if requirements["numbers"]:
        password += "".join(
            secrets.choice(string.digits) for i in range(requirements["numbers"])
        )
        subset = subset.replace(string.digits, "", 1)
        temp_len -= requirements["numbers"]

    if requirements["uppercase"]:
        password += "".join(
            secrets.choice(string.ascii_uppercase)
            for i in range(requirements["uppercase"])
        )
        subset = subset.replace(string.ascii_uppercase, "", 1)
        temp_len -= requirements["uppercase"]

    if requirements["characters"]:
        password += "".join(
            secrets.choice(string.punctuation)
            for i in range(requirements["characters"])
        )
        subset = subset.replace(string.punctuation, "", 1)
        temp_len -= requirements["characters"]

    password += "".join(secrets.choice(subset) for i in range(temp_len))

    return "".join(random.sample(password, len(password)))


def generate_passwords_to_file(n, args, subset):
    """
    Generate and save passwords to a file.

    Args:
        n (int): The number of passwords to generate and save.
        args (argparse.Namespace): Parsed command-line arguments.
        subset (str): The character subset to use for password generation.
    """
    f = open("passwords.txt", "a")

    for i in range(n):
        if args.uppercase or args.characters or args.numbers:
            requirements = {
                "uppercase": args.uppercase,
                "numbers": args.numbers,
                "characters": args.characters,
            }
            password = generate_special_password(args.length, requirements, subset)

        else:
            password = generate_password(args.length, subset)

        print(password)

        f.write(password + "\n")

    f.close()


def check_password_breach(password):
    """
    Check if a password has been involved in data breaches using the Have I Been Pwned API.

    Args:
        password (str): The password to check for breaches.

    Returns:
        int: The number of data breaches the password has been involved in.
            0 if no breaches, -1 if an API request error occurs.
    """
    # Hash the password using SHA-1
    sha1_password_hash = hashlib.sha1(password.encode()).hexdigest().upper()

    # Get the first 5 characters of the hash
    prefix = sha1_password_hash[:5]
    suffix = sha1_password_hash[5:]

    # Make a GET request to the HIBP API
    url = f"https://api.pwnedpasswords.com/range/{prefix}"
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Split the response into lines and look for a match
        hashes = [line.split(":") for line in response.text.splitlines()]
        for hash_suffix, count in hashes:
            if hash_suffix == suffix:
                return int(count)
    else:
        # Handle API request error
        print(f"Error: {response.status_code}")
        return -1

    # If no match is found, return 0 to indicate no breach
    return 0


if __name__ == "__main__":
    main()
