Usage
=====

This program has two functions: ``encrypt`` and ``decrypt``. 

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
