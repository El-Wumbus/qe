from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes
from rich import print as printf
import os
import binascii
from backports.pbkdf2 import pbkdf2_hmac
import tarfile
from sys import exit
import os.path
import shutil
import errno
from contextlib import closing
import random

class stdfile:

    def copyall(source: str, destination: str):
        """
        If the source is a file, copy it to the destination. If the source is a directory, copy it to
        the destination

        :param source: The directory you want to copy
        :type source: str
        :param destination: The destination directory where the files will be copied to
        :type destination: str
        """

        if not os.path.exists(source):
            return(1)
        if not os.path.exists(destination):
            return(1)

        try:
            shutil.copytree(source, destination)
        except OSError as exc:  # python >2.5
            if exc.errno in (errno.ENOTDIR, errno.EINVAL):
                shutil.copy(source, destination)
        else:
            raise

    def makearchive(path: str, archive_name: str):
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

    def unarchive(archive_name: str, output_path: str):
        """
        Takes an archive name and an output path, opens the archive, extracts all the files to the output
        path, and closes the archive

        :param archive_name: The name of the archive file you want to extract
        :type archive_name: str
        :param output_path: The path to the directory where you want to extract the files
        :type output_path: str
        """
        # Opening the archive, extracting all the files to the output path, and then closing the archive.
        with closing(tarfile.open(archive_name, f"r:xz")) as archive:
            archive.extractall(path=output_path)

    def tmpdir(platform: str):
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

        return(TEMPDIR)


class io:
    def ERR(message: str, code: int):
        """
        Prints a message and exits the program with a given exit code

        :param message: The message to print to the console
        :type message: str
        :param code: The exit code to exit with
        :type code: int
        """
        if message != None:
            printf(
                f"[bold red]{message} \[[bold yellow]{code}[/bold yellow]][/bold red]")
        else:
            printf("[bold red]An unknown error has occured![/bold red]")

        if code != None:
            exit(code)
        else:
            exit(1)


class crypto:
        
    def genSalt():
        """
        It generates a random string of 64 characters from the alphabet
        :return: A string of 64 random characters.
        """
        ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        chars = []
        buffer = ""
        for i in range(64):
            chars.append(random.choice(ALPHABET))
        buffer.join(chars)
        return(buffer)
        
        
    def encryptBytesToFile_AES(data, file: str, password: str):
        """
        It takes in a byte string, a file name, and a password, and then it encrypts the byte string
        with AES, and then it writes the encrypted byte string to the file

        :param data: The data to be encrypted
        :type data: bytes
        :param file: The file to write data to
        :type file: str
        :param password: The password that will be used to generate the key
        """
        # Converting the hex string to a byte string.
        salt = binascii.unhexlify(crypto.genSalt())

        # Using the PBKDF2 algorithm to generate a key from the password.
        password = password.encode("utf8")
        key = pbkdf2_hmac("sha256", password, salt, 60000, 32)

        # Encrypting the data with AES, and then getting the ciphertext and the tag.
        cipher = AES.new(key, AES.MODE_EAX)
        ciphertext, tag = cipher.encrypt_and_digest(data)

        # Opening the file in binary write mode, writing the nonce, tag, and ciphertext to the
        # file, and then closing the file.
        output_file = open(file, "wb")
        [output_file.write(x) for x in (cipher.nonce, tag, ciphertext)]
        output_file.close()

    def decryptBytesFromFile_AES(file: str, password: str):
        """
        It's using the PBKDF2 algorithm to generate a key from the password, opening the file in binary
        read mode, reading the nonce, tag, and ciphertext from the file, and then creating a cipher
        object with the key, AES.MODE_EAX, and the nonce

        :param file: The file to decrypt
        :type file: str
        :param password: The password that will be used to generate the key
        :return: The decrypted data.
        """
        # Converting the hex string to a byte string.
        salt = binascii.unhexlify(crypto.genSalt())
        # It's using the PBKDF2 algorithm to generate a key from the password.
        password = password.encode("utf8")
        key = pbkdf2_hmac("sha256", password, salt, 60000, 32)
        # Opening the file in binary read mode, reading the nonce, tag, and ciphertext from the
        # file, and then creating a cipher object with the key, AES.MODE_EAX, and the nonce.
        input_file = open(file, "rb")
        nonce, tag, ciphertext = [input_file.read(x) for x in (16, 16, -1)]
        cipher = AES.new(key, AES.MODE_EAX, nonce)

        try:
            data = cipher.decrypt_and_verify(ciphertext, tag)
            output_file = open(file, "wb")
            output_file.write(data)
            output_file.close()
            return(0)
        except:
            return(None)
        
