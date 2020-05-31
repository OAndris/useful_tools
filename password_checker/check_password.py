"""
Idea based on "Complete Python Developer in 2020: Zero to Mastery" from Andrei Neagoie.
"""

import requests
import hashlib


def request_api_data(query_char):
    # NOTE: this API returns the password hashes that start with the query_char; plus the number of times they have been pwned.
    url = f'https://api.pwnedpasswords.com/range/{query_char}'
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(f'Error fetching: {res.status_code}, check the API and try gain!')
    return res


def get_password_leaks_count(hashes, hash_to_check):
    hashes = (line.split(':') for line in hashes.text.splitlines())
    for h, count in hashes:
        if h == hash_to_check:
            return count
    return 0


def pwned_api_check(password):
    # For enhanced security (and to make the API work), convert the password to its SHA1 hash.
    # For even better security (so called "key anonymity"), do not even send the hash itself, only its first 5 characters (no chance to find it with brute force either).
    sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()  # Online tool: https://passwordsgenerator.net/sha1-hash-generator/
    first_5_char, tail = sha1password[:5], sha1password[5:]
    response_with_hashes = request_api_data(first_5_char)
    return get_password_leaks_count(response_with_hashes, tail)


def main(hide_pw_from_console=True):
    """
    Check if your passwords have ever been hacked (based on the "https://haveibeenpwned.com/" API).
    Passwords are read from "passwords.txt", separated by newline (thus they are not passed to and cannot be saved by the command line).
    They are hashed via SHA1 (thus they are converted by a one-way algorithm and not used directly),
    and only the first 5 characters of the password hash are sent to the API (thus the full hash remains unknown and the password cannot be reverse engineered with brute force).
    """
    # NOTE: typing passwords in the command line is not always secure (they might get saved), so read from file instead of using "sys.argv[1:]"
    with open('passwords.txt', 'r', encoding='utf-8') as file:
        passwords = file.read().split('\n')

    print('Checking whether your passwords have been pwned...')
    for idx, password in enumerate(passwords):
        count = pwned_api_check(password)
        password = '*'*len(password) if hide_pw_from_console else password
        if count:
            print(f" #{idx+1}: '{password}' was found {count} times... you shouldn't use this password!")
        else:
            print(f" #{idx+1}: '{password}' was NOT found. It appears to be safe!")
    print('Done!')



if __name__ == "__main__":
    main(hide_pw_from_console=True)
