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

Installation
============

.. include-start

Releases of scikit-umfpack can be installed from source using ``pip``, or with
a package manager like ``conda`` . To install from source, first ensure the
dependencies described in the next section are installed, then run::

  pip install scikit-umfpack

To install scikit-umfpack from its source code directory, run in the root of
a clone of the Git repository::

  pip install .

Dependencies
------------

scikit-umfpack depends on NumPy, SciPy, and SuiteSparse.

To build scikit-umfpack, the following are needed:
- a C compiler
- a BLAS library with CBLAS symbols (e.g., OpenBLAS, Accelerate on macOS, or reference BLAS)
- NumPy
- SuiteSparse (which contains UMFPACK)
- SWIG

pkg-config is an optional dependency, if it's installed it may be used to
detect a BLAS library.

SuiteSparse cannot be installed from PyPI, however it will likely be available
from your package manager of choice. E.g., installing on Ubuntu 22.04 can be
achieved with::

    sudo apt-get install libsuitesparse-dev

or from Conda-forge on any supported OS with::

    conda install suitesparse

SuiteSparse can also be built from source, see the instructions in the README
of the `SuiteSparse repository <https://github.com/DrTimothyAldenDavis/SuiteSparse>`__.


Detection of UMFPACK
''''''''''''''''''''

During the build, scikit-umfpack tries to automatically detect the UMFPACK
shared library and headers. In case SuiteSparse is installed in a non-standard
location, this autodetection may fail. If that happens, it is possible to
provide the paths to the library and include directories in a config file (a
Meson machine file). This file should contain absolute paths. For example, for
a conda env on Windows, it may look like:

.. code:: ini

    [properties]
    umfpack-libdir = 'C:\Users\micromamba\envs\scikit-umfpack-dev\Library\lib'
    umfpack-includedir = 'C:\Users\micromamba\envs\scikit-umfpack-dev\Library\include\suitesparse'

If that file is named ``nativefile.ini``, then the ``pip`` invocation should
look like (note that ``$PWD`` ensures an absolute path to the native file is
used)::

    pip install . -Csetup-args=--native-file=$PWD/nativefile.ini

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
