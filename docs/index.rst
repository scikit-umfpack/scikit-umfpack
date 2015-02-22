scikit-umfpack
==============

scikit-umfpack provides a wrapper of UMFPACK sparse direct solver to SciPy.

Usage:

>>> from scikits import umfpack
>>> lu = umfpack.splu(A)
>>> x = umfpack.spsolve(A, b)

Installing scikits.umfpack also enables using UMFPACK solver via some
of the scipy.sparse.linalg functions, for SciPy >= 0.14.0.

You can obtain scikit-umfpack from

- https://pypi.python.org/pypi/scikit-umfpack (releases)

- https://github.com/rc/scikit-umfpack (development version)

Contents:

.. toctree::
   :maxdepth: 1

   install
   interface
   umfpack
   develop
