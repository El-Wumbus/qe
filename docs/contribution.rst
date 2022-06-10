Contribution
============

Prerequites & Dependencies
**************************

You'll need the ``git`` version control software installed. If you
already have it installed, ensure you update it to the latest version. To
Build you will need the following:

-  `python3 <https://www.python.org/downloads/>`__
-  `pip <https://pip.pypa.io/en/stable/installation/>`__

Guidelines
**********

-  Don't change the formatting - Dont reformat or otherwise change the
   formatting of source code or documentation in the repo. Use the same
   formatting as the rest of the codebase.

-  Make documentation - If adding features or otherwise changing the
   user experience create documentation regarding the added or changed
   features.

-  Use space only indentation in all source code files with the sole
   execption of ``Makefile`` - Do not use tabs or any form of
   indentation other than spaces. Use 2 or 4 space indentation. (4 space
   indentation is perferred)

-  Format documentation - All documentation is to be written in reStructuredText
   while formatting it similar to the `this document 
   <https://github.com/El-Wumbus/qe/blob/Master/docs/contribution.rst>`__ 
   as to ensure proper consistancy and readablility.

Get the Source code
*******************

To get the source code you'll want to `fork the project on
github <https://docs.github.com/en/get-started/quickstart/fork-a-repo>`__,
then clone the fork with git. 

.. pull-quote::
   
   Note: Learn how to set up an ssh key `here <https://docs.github.com/en/authentication/connecting-to-github-with-ssh>`__, or use an http(s) link in substitution.

.. code:: bash

   git clone ssh://git@github.com/_your-username_/qe
   cd ./qe

This will download the entire repository including all revision history.

To get the lastest commits you can pull instead of redownloaing the repo
(only do this if you haven't made any changes):

.. code:: bash

   git pull

*Before* you try to commit
**************************

To give proper ownership to commits you need to configure git to give
you proper authorship. To do this you should edit your ``~/.gitconfig``
(If it doesn't exist, make it) file to include something like the
following, replacing the examples with your information of course.

.. code:: ini

   [user]
       name = john doe
       email = john.doe@example.com

Commiting
*********

First, ensure that you know a commit is a local operation and only
affects your local git repo.

check out all your changes to a sperate brach:

.. code:: bash

   git checkout -b _branch_

| Be careful to not ``git pull`` on a branch and only to do it on the
  defualt upstream branch.
| To swich branches you may use ``git checkout _branch_``. You may get
  errors when switching branches with uncommited changes, you may need
  to stash them with ``git stash``

When changing or making new files be sure to let git know to track those
files:

.. code:: bash

   git add _filename(s)_

You can add (recusrively) everything in a directoy by specifing it in
place of a file name. For example:

.. code:: bash

   git add .

The above adds everything within the current dir.

You can commit all changes with ``git commit -a``, or commit a single
file with ``git commit _filename_``. Take note that all these commits
are only local and only on your branch. If there's a commit to the
public repo then you want to rebase your changes to ensure that you're
commiting up-to-date changes. you can add a commit message with
``git commit -m "message contents"``

First get the new changes from the public repo after you ensure
``git diff`` gives no output.

.. code:: bash

   git checkout Master
   git pull
   git checkout _branch-name_
   git rebase Master

If there's no conflicts then you've rebased your branch. To push your
changes you can do something like the following:

.. code:: bash

   git push -u origin _branch_

then make a pull request in github from ``_branch_`` to merge the fork
to the ``Master`` branch of the project.
