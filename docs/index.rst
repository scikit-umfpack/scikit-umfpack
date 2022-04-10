scikit-umfpack
==============

scikit-umfpack provides a wrapper of UMFPACK sparse direct solver [1]_, [2]_,
[3]_ to SciPy.

Usage:

>>> from scikits import umfpack
>>> lu = umfpack.splu(A)
>>> x = umfpack.spsolve(A, b)

Installing scikits.umfpack also enables using UMFPACK solver via some
of the scipy.sparse.linalg functions, for SciPy >= 0.14.0.

You can obtain scikit-umfpack from

- https://pypi.python.org/pypi/scikit-umfpack (releases)

- https://github.com/scikit-umfpack/scikit-umfpack (development version)

Contents:

.. toctree::
   :maxdepth: 1

   install
   interface
   umfpack
   develop
   release

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
