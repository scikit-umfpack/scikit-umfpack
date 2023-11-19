project(
  'scikits.umfpack',
  'c',
  version: '0.4.0',
  license: 'BSD-3',
  default_options: [
    'c_std=c99',
  ]
)

fs = import('fs')
py = import('python').find_installation(pure: false)

cc = meson.get_compiler('c')

swig = find_program('swig', required: true, native: true)

blas_deps = []
if host_machine.system() == 'darwin'
  blas_deps = [dependency('Accelerate')]
else
  blas_deps = [cc.find_library('openblas', required : false)]
endif
if not blas_deps[0].found()
    blas_deps = [cc.find_library('blas')]
    cblas_dep = cc.find_library('cblas', required : false)
    if cblas_dep.found()
        blas_deps += cblas_dep
    endif
endif

# Find UMFPACK library.
# Note that Suitesparse packaging is messy; the headers may be found under
# either `<prefix>/include/` or <prefix>/suitesparse/include`. Conda-forge does
# the former, Ubuntu the latter. Usage in this package is `#include <umfpack.h>`,
# so we need to add the suitesparse/umfpack.h to the include directories.
#
# Suitesparse recently started supporting pkg-config (see
# https://github.com/DrTimothyAldenDavis/SuiteSparse/pull/356) and CMake, so try
# with `dependency()` first. Packagers that run into an issue can add a path
# below, but it'd be better if they packaged the Suitesparse .pc files.
umfpack_dep = dependency('UMFPACK', required: false)
if not umfpack_dep.found()
  # Using pkg-config or CMake didn't work, so try the "manual" way.
  # The list of paths here was taken over from numpy.distutils.system_info.py:
  _try_incdirs = [
      '/usr/include/suitesparse',
      '/usr/local/include',
      '/opt/include',
      '/opt/local/include/ufsparse',
      '/opt/local/include',
      '/sw/include',
      '/usr/include/suitesparse'
  ]
  suitesparse_incdirs = []
  umfpack_header_dirs = []
  foreach _dir : _try_incdirs
    if fs.exists(_dir)
      suitesparse_incdirs += _dir
      umfpack_header_dirs += include_directories(_dir)
    endif
  endforeach
  umfpack_lib = cc.find_library('umfpack',
      required : true,
      header_include_directories: umfpack_header_dirs,
      has_headers : ['umfpack.h']
  )
  umfpack_dep = declare_dependency(
    dependencies: umfpack_lib,
    include_directories: umfpack_header_dirs,
  )
endif

subdir('scikits')
