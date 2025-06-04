project(
  'scikits.umfpack',
  'c',
  version: '0.4.1',
  license: 'BSD-3',
  default_options: [
    'c_std=c99',
  ]
)

fs = import('fs')
py = import('python').find_installation(pure: false)

# wrapper around swig to extract includes from umfpack dependency
# future version of meson should fix this:
# https://github.com/mesonbuild/meson/issues/8334
meson_swig = fs.copyfile('meson_swig.py')

cc = meson.get_compiler('c')

swig = find_program('swig', required: true, native: true)


# The list of paths here was taken over from numpy.distutils.system_info.py:
_try_incdirs = [
    '/usr/include/suitesparse',
    '/usr/local/include',
    '/opt/include',
    '/opt/local/include/ufsparse',
    '/opt/local/include',
    '/sw/include',
    '/usr/include/suitesparse',
    '/opt/homebrew/include/suitesparse'
]
suitesparse_incdirs = []
umfpack_header_dirs = []
foreach _dir : _try_incdirs
  if fs.exists(_dir)
    suitesparse_incdirs += _dir
    umfpack_header_dirs += include_directories(_dir)
  endif
endforeach

# TODO
umfpack_libdirs = []
umfpack_libdir = meson.get_external_property('umfpack-libdir', 'UNKNOWN')
umfpack_includedir = meson.get_external_property('umfpack-includedir', 'UNKNOWN')
if umfpack_libdir != 'UNKNOWN'
    umfpack_libdirs += umfpack_libdir
endif
if umfpack_includedir != 'UNKNOWN'
    suitesparse_incdirs += umfpack_includedir
    umfpack_header_dirs += include_directories(umfpack_includedir)
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
  umfpack_lib = cc.find_library('umfpack',
      required : true,
      dirs: umfpack_libdirs,
      header_include_directories: umfpack_header_dirs,
      has_headers : ['umfpack.h']
  )
  umfpack_dep = declare_dependency(
    dependencies: umfpack_lib,
    include_directories: umfpack_header_dirs,
  )
  # Check whether we have the single-header version. May break if multiple
  # versions installed in different places.
  single_header = not cc.has_header(
    'umfpack_solve.h',
    dependencies: umfpack_dep,
    include_directories: umfpack_header_dirs
  )
else
  # pkg-config .pc files were only added to recent versions of suitesparse
  single_header = true
endif


swig_defines =[]
if single_header
  message('Using single-header UMFPACK')
  swig_defines += ['-DSK_UMFPACK_SINGLE_HEADER']
else
  message('Multiple-header UMFPACK found')
endif

blas_deps = []

# The single-header version does not need to be linked against BLAS
# This may have been from version 6.1.0 of UMFPACK (Jan 2023) as the changelog
# says BLAS symbols no longer exposed to user applications.
# Single header and int64_t is used from v6.0.0 (Nov 2022)
if not single_header
  if host_machine.system() == 'darwin'
    blas_deps = [dependency('Accelerate')]
  else
    blas_deps = [dependency('openblas', required : false)]  # try with pkg-config first
    if not blas_deps[0].found()
      blas_deps = [cc.find_library('openblas', required : false)]
    endif
  endif
  if not blas_deps[0].found()
      blas_deps = [cc.find_library('blas')]
      cblas_dep = cc.find_library('cblas', required : false)
      if cblas_dep.found()
          blas_deps += cblas_dep
      endif
  endif
endif

subdir('scikits')
