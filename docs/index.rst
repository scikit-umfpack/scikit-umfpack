scikit-umfpack
==============

scikit-umfpack provides a wrapper of UMFPACK sparse direct solver to SciPy.

Usage:

>>> from scikits import umfpack
>>> lu = umfpack.splu(A)
>>> x = umfpack.spsolve(A, b)

Installing scikits.umfpack also enables using UMFPACK solver via some
of the scipy.sparse.linalg functions, for SciPy >= 0.14.0.

Contents:

.. toctree::
   :maxdepth: 1

   install
   interface
   umfpack
   develop
