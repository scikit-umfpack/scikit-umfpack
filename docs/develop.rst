Development
===========

Code
----

``scikits.umfpack`` development is done on Github at
https://github.com/scikit-umfpack/scikit-umfpack

You can check the latest sources with the command::

  git clone https://github.com/scikit-umfpack/scikit-umfpack.git

or if you have write privileges::

  git clone git@github.com:scikit-umfpack/scikit-umfpack.git

Testing
-------

After installation, you can launch the test suite from outside the
source directory (you will need to have the ``nose`` package installed)::

    nosetests -v scikits.umfpack

Building documentation
----------------------

To build the documentation, do::

    python setup.py build_ext -i build_sphinx
