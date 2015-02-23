"""
===============
scikits.umfpack
===============

Interface to UMFPACK linear solver.

"""

from __future__ import division, print_function, absolute_import

from .umfpack import *
from .interface import *

if __doc__ is not None:
    from .umfpack import __doc__ as _umfpack_doc
    from .interface import __doc__ as _interface_doc
    __doc__ += _interface_doc
    __doc__ += _umfpack_doc
    del _umfpack_doc, _interface_doc

__all__ = [s for s in dir() if not s.startswith('_')]
from numpy.testing import Tester
test = Tester().test
