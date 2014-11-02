Install
=======

This package uses distutils, which is the default way of installing python
modules. In the directory scikit-umfpack (the same as the file you are reading
now) do::

  python setup.py install

or for a local installation::

  python setup.py install --root=<DIRECTORY>

Example site.cfg entry for UMFPACK v4.4 in <dir>::

    [amd]
    library_dirs = <dir>/UMFPACK/AMD/Lib
    include_dirs = <dir>/UMFPACK/AMD/Include
    amd_libs = amd

    [umfpack]
    library_dirs = <dir>/UMFPACK/UMFPACK/Lib
    include_dirs = <dir>/UMFPACK/UMFPACK/Include
    umfpack_libs = umfpack

    UMFPACK v5.0 (as part of UFsparse package) in <dir>:

    [amd]
    library_dirs = <dir>/UFsparse/AMD/Lib
    include_dirs = <dir>/UFsparse/AMD/Include, <dir>/UFsparse/UFconfig
    amd_libs = amd

    [umfpack]
    library_dirs = <dir>/UFsparse/UMFPACK/Lib
    include_dirs = <dir>/UFsparse/UMFPACK/Include, <dir>/UFsparse/UFconfig
    umfpack_libs = umfpack


