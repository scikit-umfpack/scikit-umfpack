project(
  'scikits.umfpack',
  'c',
  version: '0.3.4',
  license: 'BSD',
)

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
umfpack_dep = cc.find_library('umfpack', required : true,
                              has_headers : ['suitesparse/umfpack.h'])
amd_dep = cc.find_library('amd', required : true,
                          has_headers : ['suitesparse/amd.h'])

subdir('scikits')
