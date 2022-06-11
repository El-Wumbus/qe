Usage
=====

This program has four functions: ``encrypt``, ``sencrypt``, ``decrypt``, and ``sdecrypt``. 

encrypt
*******

This function takes one argument.
The function declaration:
  
.. code:: python
    
   def encrypt(filename):

- filename - The file to encrypt.

Example:
~~~~~~~~

.. code:: bash

   qe encrypt "$HOME/.zshrc"

sencrypt
********

This function takes two arguments.

1. The file to encrypt.
2. The password to encrypt the file with. 

Example:
~~~~~~~~

.. code:: bash

   qe sencrypt "$HOME/.zshrc" "3xamplepassw0rd"

decrypt
*******

This Function takes one argument. 
The function declaration:

.. code:: python

   def decrypt(filename):

- filename - The file to decrypt.

Example:
~~~~~~~~

.. code:: bash

   qe decrypt "$HOME/.zshrc"

sdecrypt
********

This function takes two arguments.

1. The file to decrypt.
2. The password to decrypt the file with. 

Example:
~~~~~~~~

.. code:: bash

   qe sdecrypt "$HOME/.zshrc" "3xamplepassw0rd"
