scikit-umfpack
==============

scikit-umfpack provides wrapper of UMFPACK sparse direct solver to SciPy.

Usage:

>>> from scikits.umfpack import spsolve, splu
>>> lu = splu(A)
>>> x = spsolve(A, b)

Installing scikits.umfpack also enables using UMFPACK solver via some
of the scipy.sparse.linalg functions, for SciPy >= 0.14.0.

Contents:

.. toctree::
   :maxdepth: 1

   install
   interface
   umfpack
   develop
