# This uses the path as is, and avoids running the interpreter.
incdir_numpy = run_command(py,['-c',
'''import os
import numpy as np
try:
  incdir = os.path.relpath(np.get_include())
except Exception:
  incdir = np.get_include()
print(incdir)
'''], check: true).stdout().strip()

_umfpack_swig = custom_target('_umfpack_swig',
    output: ['_umfpack_wrap.c'],
    input: 'umfpack.i',
    command: [swig, '-python', '-I/usr/include/suitesparse',
              '-o', '@OUTPUT@', '@INPUT@']
  )

__umfpack = py.extension_module(
    '__umfpack',
    _umfpack_swig,

    include_directories: ['/usr/include/suitesparse', incdir_numpy],
    dependencies: [blas_deps, umfpack_dep, amd_dep],
    install: true,
    subdir: 'scikits/umfpack'
)
