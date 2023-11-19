""" Test functions for UMFPACK wrappers

"""

from __future__ import division, print_function, absolute_import

import random
import unittest
import warnings

from numpy.testing import assert_array_almost_equal

from scipy.sparse import csc_matrix, linalg, spdiags, SparseEfficiencyWarning

import numpy as np
import scikits.umfpack as um


_is_32bit_platform = np.intp(0).itemsize < 8


# Force int64 index dtype even when indices fit into int32.
def _to_int64(x):
    y = csc_matrix(x).copy()
    y.indptr = y.indptr.astype(np.int64)
    y.indices = y.indices.astype(np.int64)
    return y


class _DeprecationAccept(unittest.TestCase):
    def setUp(self):
        self.mgr = warnings.catch_warnings()
        self.mgr.__enter__()

        warnings.simplefilter('ignore', SparseEfficiencyWarning)

    def tearDown(self):
        self.mgr.__exit__()


class TestScipySolvers(_DeprecationAccept):
    """Tests inverting a sparse linear system"""

    def test_solve_complex_umfpack(self):
        # Solve with UMFPACK: double precision complex
        linalg.use_solver(useUmfpack=True)
        a = self.a.astype('D')
        b = self.b
        x = linalg.spsolve(a, b)
        assert_array_almost_equal(a*x, b)

    @unittest.skipIf(_is_32bit_platform, reason="requires 64 bit platform")
    def test_solve_complex_long_umfpack(self):
        # Solve with UMFPACK: double precision complex, long indices
        linalg.use_solver(useUmfpack=True)
        a = _to_int64(self.a.astype('D'))
        b = self.b
        x = linalg.spsolve(a, b)
        assert_array_almost_equal(a*x, b)

    def test_solve_umfpack(self):
        # Solve with UMFPACK: double precision
        linalg.use_solver(useUmfpack=True)
        a = self.a.astype('d')
        b = self.b
        x = linalg.spsolve(a, b)
        assert_array_almost_equal(a*x, b)

    @unittest.skipIf(_is_32bit_platform, reason="requires 64 bit platform")
    def test_solve_long_umfpack(self):
        # Solve with UMFPACK: double precision
        linalg.use_solver(useUmfpack=True)
        a = _to_int64(self.a.astype('d'))
        b = self.b
        x = linalg.spsolve(a, b)
        assert_array_almost_equal(a*x, b)

    def test_solve_sparse_rhs(self):
        # Solve with UMFPACK: double precision, sparse rhs
        linalg.use_solver(useUmfpack=True)
        a = self.a.astype('d')
        b = csc_matrix(self.b).T
        x = linalg.spsolve(a, b)
        assert_array_almost_equal(a*x, self.b)

    def test_factorized_umfpack(self):
        # Prefactorize (with UMFPACK) matrix for solving with multiple rhs
        linalg.use_solver(useUmfpack=True)
        a = self.a.astype('d')
        solve = linalg.factorized(a)

        x1 = solve(self.b)
        assert_array_almost_equal(a*x1, self.b)
        x2 = solve(self.b2)
        assert_array_almost_equal(a*x2, self.b2)

    @unittest.skipIf(_is_32bit_platform, reason="requires 64 bit platform")
    def test_factorized_long_umfpack(self):
        # Prefactorize (with UMFPACK) matrix for solving with multiple rhs
        linalg.use_solver(useUmfpack=True)
        a = _to_int64(self.a.astype('d'))
        solve = linalg.factorized(a)

        x1 = solve(self.b)
        assert_array_almost_equal(a*x1, self.b)
        x2 = solve(self.b2)
        assert_array_almost_equal(a*x2, self.b2)

    def test_factorized_without_umfpack(self):
        # Prefactorize matrix for solving with multiple rhs
        linalg.use_solver(useUmfpack=False)
        a = self.a.astype('d')
        solve = linalg.factorized(a)

        x1 = solve(self.b)
        assert_array_almost_equal(a*x1, self.b)
        x2 = solve(self.b2)
        assert_array_almost_equal(a*x2, self.b2)

    def setUp(self):
        self.a = spdiags([[1, 2, 3, 4, 5], [6, 5, 8, 9, 10]], [0, 1], 5, 5)
        self.a2 = _to_int64(self.a)
        self.b = np.array([1, 2, 3, 4, 5], dtype=np.float64)
        self.b2 = np.array([5, 4, 3, 2, 1], dtype=np.float64)

        _DeprecationAccept.setUp(self)


class TestFactorization(_DeprecationAccept):
    """Tests factorizing a sparse linear system"""

    def test_complex_lu(self):
        # Getting factors of complex matrix
        umfpack = um.UmfpackContext("zi")

        for A in self.complex_matrices:
            umfpack.numeric(A)

            (L,U,P,Q,R,do_recip) = umfpack.lu(A)

            L = L.todense()
            U = U.todense()
            A = A.todense()
            if not do_recip:
                R = 1.0/R
            R = np.matrix(np.diag(R))
            P = np.eye(A.shape[0])[P,:]
            Q = np.eye(A.shape[1])[:,Q]

            assert_array_almost_equal(P*R*A*Q,L*U)

    @unittest.skipIf(_is_32bit_platform, reason="requires 64 bit platform")
    def test_complex_int64_lu(self):
        # Getting factors of complex matrix with long indices
        umfpack = um.UmfpackContext("zl")

        for A in self.complex_int64_matrices:
            umfpack.numeric(A)

            (L,U,P,Q,R,do_recip) = umfpack.lu(A)

            L = L.todense()
            U = U.todense()
            A = A.todense()
            if not do_recip:
                R = 1.0/R
            R = np.matrix(np.diag(R))
            P = np.eye(A.shape[0])[P,:]
            Q = np.eye(A.shape[1])[:,Q]

            assert_array_almost_equal(P*R*A*Q,L*U)

    def test_real_lu(self):
        # Getting factors of real matrix
        umfpack = um.UmfpackContext("di")

        for A in self.real_matrices:
            umfpack.numeric(A)

            (L,U,P,Q,R,do_recip) = umfpack.lu(A)

            L = L.todense()
            U = U.todense()
            A = A.todense()
            if not do_recip:
                R = 1.0/R
            R = np.matrix(np.diag(R))
            P = np.eye(A.shape[0])[P,:]
            Q = np.eye(A.shape[1])[:,Q]

            assert_array_almost_equal(P*R*A*Q,L*U)

    @unittest.skipIf(_is_32bit_platform, reason="requires 64 bit platform")
    def test_real_int64_lu(self):
        # Getting factors of real matrix with long indices
        umfpack = um.UmfpackContext("dl")

        for A in self.real_int64_matrices:
            umfpack.numeric(A)

            (L,U,P,Q,R,do_recip) = umfpack.lu(A)

            L = L.todense()
            U = U.todense()
            A = A.todense()
            if not do_recip:
                R = 1.0/R
            R = np.matrix(np.diag(R))
            P = np.eye(A.shape[0])[P,:]
            Q = np.eye(A.shape[1])[:,Q]

            assert_array_almost_equal(P*R*A*Q,L*U)

    def setUp(self):
        random.seed(0)  # make tests repeatable
        real_matrices = []
        real_matrices.append(spdiags([[1, 2, 3, 4, 5], [6, 5, 8, 9, 10]],
                                     [0, 1], 5, 5))
        real_matrices.append(spdiags([[1, 2, 3, 4, 5], [6, 5, 8, 9, 10]],
                                     [0, 1], 4, 5))
        real_matrices.append(spdiags([[1, 2, 3, 4, 5], [6, 5, 8, 9, 10]],
                                     [0, 2], 5, 5))
        real_matrices.append(np.random.rand(3,3))
        real_matrices.append(np.random.rand(5,4))
        real_matrices.append(np.random.rand(4,5))

        self.real_matrices = [csc_matrix(x).astype('d')
                              for x in real_matrices]
        self.complex_matrices = [x.astype(np.complex128)
                                 for x in self.real_matrices]

        self.real_int64_matrices = [_to_int64(x)
                                   for x in self.real_matrices]
        self.complex_int64_matrices = [_to_int64(x)
                                      for x in self.complex_matrices]

        _DeprecationAccept.setUp(self)


if __name__ == "__main__":
    unittest.main()
