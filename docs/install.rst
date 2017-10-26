Installation
============

.. include:: ../README.rst
  :start-after: include-start
  :end-before: include-end

When building from the sources, creating a ``site.cfg`` file with the
`[umfpack]` section describing location of umfpack header files and libraries
might be necessary. This file can be created next to the package's
``setup.py``.

Example site.cfg entry for UMFPACK v5.0 (as part of UFsparse package) in
<dir>::

    [amd]
    library_dirs = <dir>/UFsparse/AMD/Lib
    include_dirs = <dir>/UFsparse/AMD/Include, <dir>/UFsparse/UFconfig
    amd_libs = amd

    [umfpack]
    library_dirs = <dir>/UFsparse/UMFPACK/Lib
    include_dirs = <dir>/UFsparse/UMFPACK/Include, <dir>/UFsparse/UFconfig
    umfpack_libs = umfpack

Later versions of umfpack live in the Suitesparse package - then the ``[amd]``
section is not necessary.
