from __future__ import division, print_function, absolute_import

import warnings
import random

from numpy.testing import assert_allclose, run_module_suite
from numpy.testing.utils import WarningManager

from scipy import rand, matrix, diag, eye
from scipy.sparse import csc_matrix, spdiags, SparseEfficiencyWarning
from scipy.sparse.linalg import linsolve

import numpy as np
import scikits.umfpack as um


class TestSolvers(object):
    """Tests inverting a sparse linear system"""

    def setUp(self):
        self.a = spdiags([[1, 2, 3, 4, 5], [6, 5, 8, 9, 10]], [0, 1], 5, 5)
        self.b = np.array([1, 2, 3, 4, 5], dtype=np.float64)
        self.b2 = np.array([5, 4, 3, 2, 1], dtype=np.float64)

        self.mgr = WarningManager()
        self.mgr.__enter__()

        warnings.simplefilter("ignore", DeprecationWarning)
        warnings.simplefilter('ignore', SparseEfficiencyWarning)

    def tearDown(self):
        self.mgr.__exit__()

    def test_solve_complex_umfpack(self):
        # Solve with UMFPACK: double precision complex
        a = self.a.astype('D')
        b = self.b
        x = um.spsolve(a, b)
        assert_allclose(a*x, b)

    def test_solve_umfpack(self):
        # Solve with UMFPACK: double precision
        a = self.a.astype('d')
        b = self.b
        x = um.spsolve(a, b)
        assert_allclose(a*x, b)

    def test_solve_sparse_rhs(self):
        # Solve with UMFPACK: double precision, sparse rhs
        a = self.a.astype('d')
        b = csc_matrix(self.b).T
        x = um.spsolve(a, b)
        assert_allclose(a*x, self.b)

    def test_splu_solve(self):
        # Prefactorize (with UMFPACK) matrix for solving with multiple rhs
        a = self.a.astype('d')
        lu = um.splu(a)

        x1 = lu.solve(self.b)
        assert_allclose(a*x1, self.b)
        x2 = lu.solve(self.b2)
        assert_allclose(a*x2, self.b2)

    def test_splu_lu(self):
        A = csc_matrix([[1,2,0,4],[1,0,0,1],[1,0,2,1],[2,2,1,0.]])

        lu = um.splu(A)

        Pr = csc_matrix((4, 4))
        Pr[lu.perm_r, np.arange(4)] = 1
        Pc = csc_matrix((4, 4))
        Pc[np.arange(4), lu.perm_c] = 1

        R = csc_matrix((4, 4))
        R.setdiag(lu.R)

        A2 = (R * Pr.T * (lu.L * lu.U) * Pc.T).A

        assert_allclose(A2, A.A, atol=1e-13)
