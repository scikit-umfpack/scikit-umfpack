scikit-umfpack
==============

`scikit-umfpack <https://scikit-umfpack.github.io/scikit-umfpack>`_ provides
wrapper of UMFPACK sparse direct solver to SciPy.

Usage:

.. code:: python

    >>> from scikits.umfpack import spsolve, splu
    >>> lu = splu(A)
    >>> x = spsolve(A, b)

Installing scikits.umfpack also enables using UMFPACK solver via some of
the scipy.sparse.linalg functions, for SciPy >= 0.14.0. Note you will
need to have installed UMFPACK before hand. UMFPACK is a part of
`SuiteSparse <http://faculty.cse.tamu.edu/davis/suitesparse.html>`__.

References
----------

.. [1] T. A. Davis, Algorithm 832: UMFPACK - an unsymmetric-pattern
       multifrontal method with a column pre-ordering strategy, ACM Trans. on
       Mathematical Software, 30(2), 2004, pp. 196--199.
       https://dl.acm.org/doi/abs/10.1145/992200.992206
.. [2] P. Amestoy, T. A. Davis, and I. S. Duff, Algorithm 837: An approximate
       minimum degree ordering algorithm, ACM Trans. on Mathematical Software,
       30(3), 2004, pp. 381--388.
       https://dl.acm.org/doi/abs/10.1145/1024074.1024081
.. [3] T. A. Davis, J. R. Gilbert, S. Larimore, E. Ng, Algorithm 836: COLAMD,
       an approximate column minimum degree ordering algorithm, ACM Trans. on
       Mathematical Software, 30(3), 2004, pp. 377--380.
       https://doi.org/10.1145/1024074.1024080

Dependencies
============

scikit-umfpack depends on NumPy, SciPy, SuiteSparse, and swig is a
build-time dependency.

Building SuiteSparse
--------------------

SuiteSparse may be available from your package manager or as a prebuilt
shared library. If that is the case use that if possible. Installation
on Ubuntu 14.04 can be achieved with

::

    sudo apt-get install libsuitesparse-dev

Otherwise, you will need to build from source. Unfortunately,
SuiteSparse's makefiles do not support building a shared library out of
the box. You may find `Stefan Fuertinger instructions
helpful <http://fuertinger.lima-city.de/research.html#building-numpy-and-scipy>`__.

Furthmore, building METIS-4.0, an optional but important compile time
dependency of SuiteSparse, has problems on newer GCCs. This `patch and
instructions <http://www.math-linux.com/mathematics/linear-systems/article/how-to-patch-metis-4-0-error-conflicting-types-for-__log2>`__
from Nadir Soualem are helpful for getting a working METIS build.

Otherwise, I commend you to the documentation.

Installation
============

.. include-start

Releases of scikit-umfpack can be installed using ``pip``. For a system-wide
installation run::

  pip install --upgrade scikit-umfpack

or for a user installation run ::

  pip install --upgrade --user scikit-umfpack

To install scikit-umfpack from its source code directory, run in that
directory (``--user`` means a user installation)::

  pip install --upgrade --user .

.. include-end

Development
===========

Code
----

You can check the latest sources with the command:

::

    git clone https://github.com/scikit-umfpack/scikit-umfpack.git

or if you have write privileges:

::

    git clone git@github.com:scikit-umfpack/scikit-umfpack.git

Testing
-------

After installation, you can launch the test suite from outside the source
directory (you will need to have the ``pytest`` package installed):

::

   pip install pytest
   pytest --pyargs scikits.umfpack
