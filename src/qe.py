#!/usr/bin/env python3
"""
quick encryption is a program that encrypts(with 256bit-AES) and decrypts
files in a single command by usage of a passphrase.
"""

import os
import sys
import getopt
from getpass import getpass
from rich import print as printf
from rich.traceback import install
from lib import die, Crypto

PROGRAM_NAME = "qe"
# Creating an instance of the Crypto class.
crypto = Crypto()

# Installing the rich traceback module.
install()


def usage():
    """
    It prints the usage of the program
    """
    printf(
        f"usage:: [bold #5865F2]{PROGRAM_NAME}[/] (encrypt/decrypt) \"filename\"")


def encrypt(filename, passwd=None):
    """
    It encrypts a file with a password

    :param filename: The name of the file to encrypt
    """
    # Checking if the file exists and if it is a file. If it doesn't exist, it prints an error
    # message. If it isn't a file, it prints an error message.
    if not os.path.exists(filename):
        die(f"No such file or directory: \"{filename}\"", 1)
    if not os.path.isfile(filename):
        die(f"\"{filename}\" is not a file", 1)

    # Checking if the password is None. If it is, it gets the password from the user.
    if passwd is None:
        passwd = getpass(prompt="Enter a password for encryption: ")
    # Opening the file in binary mode, reading the contents of the file, and then closing the file.
    file = open(filename, "rb")
    file_contents = file.read()
    file.close()

    # Encrypting the file contents with the password and then writing encrypted data to the file.
    crypto.encrypt_bytes_to_file_aes(file_contents, filename, passwd)


def decrypt(filename, passwd=None):
    """
    It decrypts a file using a password

    :param filename: The name of the file to be decrypted
    :return: The return value is the exit code of the program.
    """
    # Checking if the file exists and if it is a file. If it doesn't exist, it prints an error
    # message. If it isn't a file, it prints an error message.
    if not os.path.exists(filename):
        die(f"No such file or directory: \"{filename}\"", 1)
    if not os.path.isfile(filename):
        die(f"\"{filename}\" is not a file", 1)

    # Checking if the password is None. If it is, it gets the password from the user.
    if passwd is None:
        passwd = getpass(prompt="Enter a password for decryption: ")

    # Checking if the decryption function returns None. If it does, it returns 1.
    if crypto.decrypt_bytes_to_file_aes(filename, passwd) is None:
        return 1

    return 0


def main():
    """
    It checks if the user has passed the -h or --help option, if they have, it prints the usage of
    the program. If they haven't, it checks if the number of arguments is less than or equal to 0.
    If it is, print an error message. If it isn't, it checks if the user has passed the encrypt
    argument. If they have, it checks if the number of arguments is less than 2. If it is, it prints
    an error message. If it isn't, it calls the encrypt function with the filename as the argument.
    If the user hasn't passed the encrypt argument, it checks if the user has passed the decrypt or
    unencrypt argument. If they have, it checks if the number of arguments is less than 2. If it is,
    it prints an error message. If it isn't, it calls the decrypt function with the filename as the
    argument. If the user hasn't passed an appropriate argument, it prints an error message.

    :return: The return value is the exit code of the program.
    """
    # Getting the options and arguments passed by the user.
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h", ["help"])
        argsc = len(args)
    # Catching the error that is thrown by the getopt module.
    except getopt.GetoptError as err:
        die(f"Getops Error: {err}", 2)

    # Checking if the user has passed the -h or --help option. If they have, it prints the usage of
    # the program.
    for opt in opts:
        if opt in ["-h", "--help"]:
            usage()
            return 0

        else:
            # If the option isn't handled, print an error message.
            assert False, "unhandled option"

   # Checking if the number of arguments is less than or equal to 0. If it is, it prints an error
   # message.
    if argsc <= 0:
        die("Not enough arguments", 2)

    # Checking if the user has passed the encrypt argument. If they have, it checks if the number of
    # arguments is less than 2. If it is, it prints an error message. If it isn't, it calls the
    # encrypt function with the filename as the argument.
    if args[0] == "encrypt":
        # Checking if the number of arguments is less than 2. If it is, it prints an error message.
        if argsc < 2:
            die(
                "Too few arguments for function [bold #5865F2]encrypt[/]", 2)

        # Calling the encrypt function with the filename as the argument.
        filename = args[1]
        encrypt(filename)
        return 0

    # Checking if the user has passed the decrypt or unencrypt argument. If they have, it
    # checks if the number of arguments is less than 2. If it is, it prints an error message.
    # If it isn't, it calls the decrypt function with the filename as the argument.

    if args[0] == "decrypt" or args[0] == "unencrypt":
        # Checking if the number of arguments is less than 2. If it is, it prints an error message.
        if argsc < 2:
            die(
                "Too few arguments for function [bold #5865F2]decrypt[/]", 2)

        # Calling the decrypt function with the filename as the argument.
        filename = args[1]
        if decrypt(filename):
            die("Decrypting failed! Password may be incorrect.", 1)
        return 0

    if args[0] == "sdecrypt" or args[0] == "sunencrypt":
        # Checking if the number of arguments is less than 2. If it is, it prints an error message.
        if argsc < 3:
            die(
                "Too few arguments for function [bold #5865F2]sdecrypt[/]", 2)

        # Calling the decrypt function with the filename as the argument.
        filename = args[1]
        password = args[2]
        if decrypt(filename, passwd=password):
            die("Decrypting failed! Password may be incorrect.", 1)
        return 0

    if args[0] == "sencrypt":
        # Checking if the number of arguments is less than 2. If it is, it prints an error message.
        if argsc < 2:
            die(
                "Too few arguments for function [bold #5865F2]sencrypt[/]", 2)

        # Calling the encrypt function with the filename as the argument.
        filename = args[1]
        password = args[2]
        encrypt(filename, passwd=password)
        return 0

    die(f"function {args[0]} not recognized", 1)


if __name__ == "__main__":
    sys.exit(main())
