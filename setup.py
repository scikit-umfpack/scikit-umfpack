#!/usr/bin/env python

descr = """Python interface to UMFPACK sparse direct solver."""

DISTNAME            = 'scikit-umfpack'
DESCRIPTION         = 'Python interface to UMFPACK sparse direct solver.'
LONG_DESCRIPTION    = open('README.rst').read()
MAINTAINER          = 'Robert Cimrman'
MAINTAINER_EMAIL    = 'cimrman3@ntc.zcu.cz'
URL                 = 'https://scikit-umfpack.github.io/scikit-umfpack'
LICENSE             = 'BSD'
DOWNLOAD_URL        = URL
VERSION             = '0.3.1'
ISRELEASED          = False

import sys
import os
import shutil
import subprocess
from distutils.command.clean import clean as Clean

# Return the git revision as a string
def git_version():
    def _minimal_ext_cmd(cmd):
        # construct minimal environment
        env = {}
        for k in ['SYSTEMROOT', 'PATH']:
            v = os.environ.get(k)
            if v is not None:
                env[k] = v
        # LANGUAGE is used on win32
        env['LANGUAGE'] = 'C'
        env['LANG'] = 'C'
        env['LC_ALL'] = 'C'
        out = subprocess.Popen(cmd, stdout=subprocess.PIPE, env=env).communicate()[0]
        return out

    try:
        out = _minimal_ext_cmd(['git', 'rev-parse', 'HEAD'])
        GIT_REVISION = out.strip().decode('ascii')
    except OSError:
        GIT_REVISION = "Unknown"

    return GIT_REVISION

def get_version_info():
    # Adding the git rev number needs to be done inside
    # write_version_py(), otherwise the import of scikits.umfpack.version messes
    # up the build under Python 3.
    FULLVERSION = VERSION
    if os.path.exists('.git'):
        GIT_REVISION = git_version()
    elif os.path.exists('scikits/umfpack/version.py'):
        # must be a source distribution, use existing version file
        # load it as a separate module to not load scikits/umfpack/__init__.py
        import imp
        version = imp.load_source('scikits.umfpack.version',
                                  'scikits/umfpack/version.py')
        GIT_REVISION = version.git_revision
    else:
        GIT_REVISION = "Unknown"

    if not ISRELEASED:
        FULLVERSION += '.dev0+' + GIT_REVISION[:7]

    return FULLVERSION, GIT_REVISION

def write_version_py(filename='scikits/umfpack/version.py'):
    cnt = """# THIS FILE IS GENERATED FROM scikit-umfpack SETUP.PY
short_version = '%(version)s'
version = '%(version)s'
full_version = '%(full_version)s'
git_revision = '%(git_revision)s'
release = %(isrelease)s

if not release:
    version = full_version
"""
    FULLVERSION, GIT_REVISION = get_version_info()

    a = open(filename, 'w')
    try:
        a.write(cnt % {'version': VERSION,
                       'full_version': FULLVERSION,
                       'git_revision': GIT_REVISION,
                       'isrelease': str(ISRELEASED)})
    finally:
        a.close()

###############################################################################
# Optional setuptools features
# We need to import setuptools early, if we want setuptools features,
# as it monkey-patches the 'setup' function

# For some commands, use setuptools
if len(set(('develop', 'release', 'bdist_egg', 'bdist_rpm',
           'bdist_wininst', 'install_egg_info', 'build_sphinx',
           'egg_info', 'easy_install', 'upload', 'bdist_wheel',
           '--single-version-externally-managed',
            )).intersection(sys.argv)) > 0:
    import setuptools
    extra_setuptools_args = dict(
        zip_safe=False,  # the package can run out of an .egg file
        include_package_data=True,
    )
else:
    extra_setuptools_args = dict()


###############################################################################

class CleanCommand(Clean):
    description = 'Remove build directories, and compiled file in the source tree'

    def run(self):
        Clean.run(self)
        if os.path.exists('build'):
            shutil.rmtree('build')
        for dirpath, dirnames, filenames in os.walk('umfpack'):
            for filename in filenames:
                if (filename.endswith('.so') or filename.endswith('.pyd')
                             or filename.endswith('.dll')
                             or filename.endswith('.pyc')):
                    os.unlink(os.path.join(dirpath, filename))
            for dirname in dirnames:
                if dirname == '__pycache__':
                    shutil.rmtree(os.path.join(dirpath, dirname))

###############################################################################
def configuration(parent_package='', top_path=None):
    if os.path.exists('MANIFEST'): os.remove('MANIFEST')

    from numpy.distutils.misc_util import Configuration
    config = Configuration(None, parent_package, top_path)

    # Avoid non-useful msg:
    # "Ignoring attempt to set 'name' (from ... "
    config.set_options(ignore_setup_xxx_py=True,
                       assume_default_configuration=True,
                       delegate_options_to_subpackages=True,
                       quiet=True)

    config.add_subpackage('scikits.umfpack')
    config.add_data_files('scikits/__init__.py')
    config.add_data_files('MANIFEST.in')

    return config

def setup_package():
    # Rewrite the version file every time
    write_version_py()

    cmdclass = {'clean': CleanCommand}
    try:
        from sphinx.setup_command import BuildDoc as SphinxBuildDoc
        class BuildDoc(SphinxBuildDoc):
            """Run in-place build before Sphinx doc build"""
            def run(self):
                ret = subprocess.call([sys.executable, sys.argv[0], 'build_ext', '-i'])
                if ret != 0:
                    raise RuntimeError("Building failed!")
                SphinxBuildDoc.run(self)
        cmdclass['build_sphinx'] = BuildDoc
    except ImportError:
        pass

    if not 'sdist' in sys.argv[1:]:
        try:
            from setuptools.command.test import test as TestCommand
            class NoseTestCommand(TestCommand):
                def finalize_options(self):
                    TestCommand.finalize_options(self)
                    self.test_args = []
                    self.test_suite = True

                def run_tests(self):
                    # Run nose ensuring that argv simulates running nosetests directly
                    ret = subprocess.call([sys.executable, sys.argv[0], 'build_ext', '-i'])
                    if ret != 0:
                        raise RuntimeError("Building failed!")
                    import nose
                    nose.run_exit(argv=['nosetests'])
            cmdclass['test'] = NoseTestCommand
        except ImportError:
            pass

    try:
        import numpy
        INSTALL_REQUIRES = [
            'numpy>=' + str(numpy.__version__),
            'scipy>=1.0.0rc1',
        ]
    except ImportError:
        INSTALL_REQUIRES = []

    metadata = dict(name=DISTNAME,
                    maintainer=MAINTAINER,
                    maintainer_email=MAINTAINER_EMAIL,
                    description=DESCRIPTION,
                    license=LICENSE,
                    url=URL,
                    version=VERSION,
                    download_url=DOWNLOAD_URL,
                    long_description=LONG_DESCRIPTION,
                    install_requires=INSTALL_REQUIRES,
                    classifiers=[
                        'Development Status :: 4 - Beta',
                        'Environment :: Console',
                        'Intended Audience :: Developers',
                        'Intended Audience :: Science/Research',
                        'License :: OSI Approved :: BSD License',
                        'Topic :: Scientific/Engineering',
                        'Programming Language :: C',
                        'Programming Language :: Python',
                        'Topic :: Software Development',
                        'Topic :: Scientific/Engineering',
                        'Operating System :: Microsoft :: Windows',
                        'Operating System :: POSIX',
                        'Operating System :: Unix',
                        'Operating System :: MacOS',
                    ],
                    platforms = ['Linux', 'Mac OS-X', 'Windows'],
                    test_suite='nose.collector',
                    cmdclass=cmdclass,
                    **extra_setuptools_args)

    if (len(sys.argv) >= 2
            and ('--help' in sys.argv[1:] or sys.argv[1]
                 in ('--help-commands', 'egg_info', '--version', 'clean'))):

        # For these actions, NumPy is not required.
        #
        # They are required to succeed without Numpy for example when
        # pip is used to install Scikit when Numpy is not yet present in
        # the system.
        try:
            from setuptools import setup
        except ImportError:
            from distutils.core import setup

        metadata['version'] = VERSION
    else:
        from numpy.distutils.core import setup

        metadata['configuration'] = configuration

    setup(**metadata)

if __name__ == '__main__':
    setup_package()
