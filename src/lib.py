"""It's a class that contains functions that are used to do various things"""

import os
import os.path
import tarfile
import shutil
import errno
from contextlib import closing
import random
import sys
from Cryptodome.Cipher import AES
from rich import print as printf
from backports.pbkdf2 import pbkdf2_hmac


def die(message: str, code: int):
    """
    Prints a message and exits the program with a given exit code
    :param message: The message to print to the console
    :type message: str
    :param code: The exit code to exit with
    :type code: int
    """
    if message is not None:
        printf(
            f"[bold red]{message} ([bold yellow]{code}[/bold yellow])[/bold red]")
    else:
        printf("[bold red]An unknown error has occured![/bold red]")
    if code is not None:
        sys.exit(code)
    else:
        sys.exit(1)


class StdFile:
    """
    This class is a collection of functions that are used to manipulate files and directories
    """

    def __init__(self):
        pass

    def copyall(self, source: str, destination: str):
        """
        If the source is a file, copy it to the destination. If the source is a directory, copy it
        to the destination

        :param source: The directory you want to copy
        :type source: str
        :param destination: The destination directory where the files will be copied to
        :type destination: str
        """

        if not os.path.exists(source):
            return 1
        if not os.path.exists(destination):
            return 1

        try:
            shutil.copytree(source, destination)
        except OSError as exc:  # python >2.5
            if exc.errno in (errno.ENOTDIR, errno.EINVAL):
                shutil.copy(source, destination)
            else:
                return 1
        return 0

    def makearchive(self, path: str, archive_name: str):
        """
        Takes a path to a directory, an archive name, and creates a tar archive
        of the directory with xz compresion

        :param path: The path to the directory you want to archive
        :type path: str
        :param archive_name: The name of the archive you want to create
        :type archive_name: str
        :type compression_mode: str
        """

        # Creating a tarfile object, and then adding the path to the tarfile object.
        with tarfile.open(archive_name, "w:xz") as tar:
            tar.add(path, arcname=os.path.basename(path))

    def unarchive(self, archive_name: str, output_path: str):
        """
        Takes an archive name and an output path, opens the archive, extracts all the files to the
        output path, and closes the archive

        :param archive_name: The name of the archive file you want to extract
        :type archive_name: str
        :param output_path: The path to the directory where you want to extract the files
        :type output_path: str
        """
        # Opening the archive, extracting all the files to output_path, then closing the archive.
        with closing(tarfile.open(archive_name, "r:xz")) as archive:
            archive.extractall(path=output_path)

    def tmpdir(self, platform: str):
        """
        This function returns the temporary directory for the current operating system

        :param platform: The platform you're running on
        :type platform: str
        :return: the TEMPDIR variable.
        """

        # Find tmp dir
        if platform != "Windows":
            TEMPDIR = '/tmp'
        else:
            TEMPDIR = os.path.expanduser("~\\AppData\\Local\\Temp")

        return TEMPDIR


class Crypto:

    """Cryptgraphic functions
    """

    def __init__(self):
        pass

    def gen_salt(self):
        """
        It creates a random string of 64 characters, converts it to a byte array, and returns it
        :return: A string of 64 random characters
        """
        alphabet = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        chars = []
        i = 1
        while i <= 64:
            chars.append(random.choice(alphabet))
            i += 1
        buffer = "".join(chars).encode('utf-8')
        return buffer

    def encrypt_bytes_to_file_aes(self, data, file: str, password: str):
        """
        It takes in a byte string, a file name, and a password, and then it encrypts the byte string
        with AES, and then it writes the encrypted byte string to the file

        :param data: The data to be encrypted
        :type data: bytes
        :param file: The file to write data to
        :type file: str
        :param password: The password that will be used to generate the key
        """
        # Get the salt
        salt = self.gen_salt()

        # Using the PBKDF2 algorithm to generate a key from the password.
        password = password.encode("utf8")
        key = pbkdf2_hmac("sha256", password, salt, 60000, 32)

        # Encrypting the data with AES, and then getting the ciphertext and the tag.
        cipher = AES.new(key, AES.MODE_EAX)
        ciphertext, tag = cipher.encrypt_and_digest(data)

        # Opening the file in binary write mode, writing the nonce, tag, and ciphertext to the
        # file, and then closing the file.
        output_file = open(file, "wb")
        for text in (salt, cipher.nonce, tag, ciphertext):
            output_file.write(text)
        output_file.close()

    def decrypt_bytes_to_file_aes(self, file: str, password: str):
        """
        It's using the PBKDF2 algorithm to generate a key from the password, opening the file in
        binary read mode, reading the nonce, tag, and ciphertext from the file, and then creating
        a cipher object with the key, AES.MODE_EAX, and the nonce.

        :param file: The file to decrypt
        :type file: str
        :param password: The password that will be used to generate the key
        :return: The decrypted data.
        """

        # It's opening the file in binary read mode, reading the salt, nonce, tag, and ciphertext
        # from the file, and then creating a cipher object with the key, AES.MODE_EAX, and the nonce
        input_file = open(file, "rb")
        salt, nonce, tag, ciphertext = [
            input_file.read(x) for x in (64, 16, 16, -1)]

        # Converting the password to a byte array.
        password = password.encode("utf8")

        # Using the PBKDF2 algorithm to generate a key from the password.
        key = pbkdf2_hmac("sha256", password, salt, 60000, 32)

        # Creating a cipher object with the key, AES.MODE_EAX, and the nonce.
        cipher = AES.new(key, AES.MODE_EAX, nonce)

        try:
            # Decrypting the ciphertext with the cipher object, and then it's verifying the tag.
            data = cipher.decrypt_and_verify(ciphertext, tag)

            # Writing the decrypted data to the file.
            output_file = open(file, "wb")
            output_file.write(data)
            output_file.close()

            return 0   # Return Success
        except Exception:
            return 1  # Return Failure
