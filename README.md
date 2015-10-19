scikit-umfpack
==============

scikit-umfpack provides wrapper of UMFPACK sparse direct solver to SciPy.

Usage:

```python
>>> from scikits.umfpack import spsolve, splu
>>> lu = splu(A)
>>> x = spsolve(A, b)
```

Installing scikits.umfpack also enables using UMFPACK solver via some
of the scipy.sparse.linalg functions, for SciPy >= 0.14.0. Note you will need to
have installed UMFPACK before hand. UMFPACK is parse of
[SuiteSparse](http://faculty.cse.tamu.edu/davis/suitesparse.html).


Dependencies
============

scikit-umfpack depends on NumPy, SciPy, SuiteSparse, and swig is a build-time
dependency.


Building SuiteSparse
--------------------

SuiteSparse may be available from your package manager or as a prebuilt shared
library. If that is the case use that if possible. Installation on Ubuntu 14.04
can be achieved with

```
sudo apt-get install libsuitesparse-dev
```

Otherwise, you will need to build from source. Unfortunately, SuiteSparse's
makefiles do not support building a shared library out of the box. You may find
[Stefan Fürtinger instructions
helpful](http://fuertinger.lima-city.de/research.html#building-numpy-and-scipy).

Furthmore, building METIS-4.0, an optional but important compile time
dependency of SuiteSparse, has problems on newer GCCs. This [patch and
instructions](http://www.math-linux.com/mathematics/linear-systems/article/how-to-patch-metis-4-0-error-conflicting-types-for-\_\_log2)
from Nadir Soualem are helpful for getting a working METIS build.

Otherwise, I commend you to the documentation.


Install
=======

This package uses distutils, which is the default way of installing python
modules. In the directory scikit-umfpack (the same as the file you are reading
now) do:

```
python setup.py install
```

or for a local installation:

```
python setup.py install --root=<DIRECTORY>
```

Development
===========

Code
----

You can check the latest sources with the command:

```
git clone https://github.com/scikit-umfpack/scikit-umfpack.git
```

or if you have write privileges:

```
git clone git@github.com:scikit-umfpack/scikit-umfpack.git
```

Testing
-------

After installation, you can launch the test suite from outside the
source directory (you will need to have the ``nose`` package installed):

```
nosetests -v scikits.umfpack
```
