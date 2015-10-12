"""
Easy-to-use UMFPACK interface
=============================

.. currentmodule:: scikits.umfpack

The following functions can be used for LU decompositions and solving
equation systems:

.. autosummary::
   :toctree: reference/

   spsolve
   splu
   UmfpackLU

"""

from __future__ import division, print_function, absolute_import

from warnings import warn
import sys
import numpy as np
from numpy import asarray, empty, ravel, nonzero
from scipy.sparse import (isspmatrix_csc, isspmatrix_csr, isspmatrix,
                          SparseEfficiencyWarning, csc_matrix, hstack)

from .umfpack import UmfpackContext, UMFPACK_A


__all__ = ['spsolve', 'splu', 'UmfpackLU']


if sys.version_info[0] >= 3:
    xrange = range


def spsolve(A, b):
    """Solve the sparse linear system Ax=b, where b may be a vector or a matrix.

    Parameters
    ----------
    A : ndarray or sparse matrix
        The square matrix A will be converted into CSC or CSR form
    b : ndarray or sparse matrix
        The matrix or vector representing the right hand side of the equation.

    Returns
    -------
    x : ndarray or sparse matrix
        the solution of the sparse linear equation.
        If b is a vector, then x is a vector of size A.shape[0]
        If b is a matrix, then x is a matrix of size (A.shape[0],)+b.shape[1:]

    """
    x = UmfpackLU(A).solve(b)

    if b.ndim == 2 and b.shape[1] == 1:
        # compatibility with scipy.sparse.spsolve quirk
        return x.ravel()
    else:
        return x


def splu(A):
    """
    Compute the LU decomposition of a sparse, square matrix.

    Parameters
    ----------
    A : sparse matrix
        Sparse matrix to factorize. Should be in CSR or CSC format.

    Returns
    -------
    invA : scikits.umfpack.UmfpackLU
        Object, which has a ``solve`` method.

    Notes
    -----
    This function uses the UMFPACK library.

    """
    return UmfpackLU(A)


class UmfpackLU(object):
    """
    LU factorization of a sparse matrix.

    Factorization is represented as::

        Pr * (R^-1) * A * Pc = L * U

    Parameters
    ----------
    A : csc_matrix or csr_matrix
        Matrix to decompose

    Attributes
    ----------
    shape
    nnz
    perm_c
    perm_r
    L
    U
    R

    Methods
    -------
    solve
    solve_sparse

    Examples
    --------
    The LU decomposition can be used to solve matrix equations. Consider:

    >>> import numpy as np
    >>> from scipy.sparse import csc_matrix
    >>> from scikits import umfpack
    >>> A = csc_matrix([[1,2,0,4],[1,0,0,1],[1,0,2,1],[2,2,1,0.]])

    This can be solved for a given right-hand side:

    >>> lu = umfpack.splu(A)
    >>> b = np.array([1, 2, 3, 4])
    >>> x = lu.solve(b)
    >>> A.dot(x)
    array([ 1.,  2.,  3.,  4.])

    The ``lu`` object also contains an explicit representation of the
    decomposition. The permutations are represented as mappings of
    indices:

    >>> lu.perm_r
    array([0, 2, 1, 3], dtype=int32)
    >>> lu.perm_c
    array([2, 0, 1, 3], dtype=int32)

    The L and U factors are sparse matrices in CSC format:

    >>> lu.L.A
    array([[ 1. ,  0. ,  0. ,  0. ],
           [ 0. ,  1. ,  0. ,  0. ],
           [ 0. ,  0. ,  1. ,  0. ],
           [ 1. ,  0.5,  0.5,  1. ]])
    >>> lu.U.A
    array([[ 2.,  0.,  1.,  4.],
           [ 0.,  2.,  1.,  1.],
           [ 0.,  0.,  1.,  1.],
           [ 0.,  0.,  0., -5.]])

    The permutation matrices can be constructed:

    >>> Pr = csc_matrix((4, 4))
    >>> Pr[lu.perm_r, np.arange(4)] = 1
    >>> Pc = csc_matrix((4, 4))
    >>> Pc[np.arange(4), lu.perm_c] = 1

    Similarly for the row scalings:

    >>> R = csc_matrix((4, 4))
    >>> R.setdiag(lu.R)

    We can reassemble the original matrix:

    >>> (Pr.T * R * (lu.L * lu.U) * Pc.T).A
    array([[ 1.,  2.,  0.,  4.],
           [ 1.,  0.,  0.,  1.],
           [ 1.,  0.,  2.,  1.],
           [ 2.,  2.,  1.,  0.]])
    """

    def __init__(self, A):
        if not (isspmatrix_csc(A) or isspmatrix_csr(A)):
            A = csc_matrix(A)
            warn('spsolve requires A be CSC or CSR matrix format',
                    SparseEfficiencyWarning)

        A.sort_indices()
        A = A.asfptype()  # upcast to a floating point format

        M, N = A.shape
        if (M != N):
            raise ValueError("matrix must be square (has shape %s)" % ((M, N),))

        if A.dtype.char not in 'dD':
            raise ValueError("Only double precision matrices supported")

        family = {'d': 'di', 'D': 'zi'}
        self.umf = UmfpackContext(family[A.dtype.char])
        self.umf.numeric(A)

        self._A = A
        self._L = None
        self._U = None
        self._P = None
        self._Q = None
        self._R = None

    def solve(self, b):
        """
        Solve linear equation A x = b for x

        Parameters
        ----------
        b : ndarray
            Right-hand side of the matrix equation. Can be vector or a matrix.

        Returns
        -------
        x : ndarray
            Solution to the matrix equation

        """
        if isspmatrix(b):
            b = b.toarray()

        if b.shape[0] != self._A.shape[1]:
            raise ValueError("Shape of b is not compatible with that of A")

        b_arr = asarray(b, dtype=self._A.dtype).reshape(b.shape[0], -1)
        x = np.zeros((self._A.shape[0], b_arr.shape[1]), dtype=self._A.dtype)
        for j in range(b_arr.shape[1]):
            x[:,j] = self.umf.solve(UMFPACK_A, self._A, b_arr[:,j], autoTranspose=True)
        return x.reshape((self._A.shape[0],) + b.shape[1:])

    def solve_sparse(self, B):
        """
        Solve linear equation of the form A X = B. Where B and X are sparse matrices.

        Parameters
        ----------
        B : any scipy.sparse matrix
            Right-hand side of the matrix equation.
            Note: it will be converted to csc_matrix via `.tocsc()`.

        Returns
        -------
        X : csc_matrix
            Solution to the matrix equation as a csc_matrix
        """
        B = B.tocsc()
        cols = list()
        for j in xrange(B.shape[1]):
            col = self.solve(B[:,j])
            cols.append(csc_matrix(col))
        return hstack(cols)

    def _compute_lu(self):
        if self._L is None:
            self._L, self._U, self._P, self._Q, self._R, do_recip = self.umf.lu(self._A)
            if do_recip:
                with np.errstate(divide='ignore'):
                    np.reciprocal(self._R, out=self._R)

            # Conform to scipy.sparse.splu convention on permutation matrices
            self._P = self._P[self._P]

    @property
    def shape(self):
        """
        Shape of the original matrix as a tuple of ints.
        """
        return self._A.shape

    @property
    def L(self):
        """
        Lower triangular factor with unit diagonal as a
        `scipy.sparse.csc_matrix`.
        """
        self._compute_lu()
        return self._L

    @property
    def U(self):
        """
        Upper triangular factor as a `scipy.sparse.csc_matrix`.
        """
        self._compute_lu()
        return self._U

    @property
    def R(self):
        """
        Row scaling factors, as a 1D array.
        """
        self._compute_lu()
        return self._R

    @property
    def perm_c(self):
        """
        Permutation Pc represented as an array of indices.

        The column permutation matrix can be reconstructed via:

        >>> Pc = np.zeros((n, n))
        >>> Pc[np.arange(n), perm_c] = 1
        """
        self._compute_lu()
        return self._Q

    @property
    def perm_r(self):
        """
        Permutation Pr represented as an array of indices.

        The row permutation matrix can be reconstructed via:

        >>> Pr = np.zeros((n, n))
        >>> Pr[perm_r, np.arange(n)] = 1
        """
        self._compute_lu()
        return self._P

    @property
    def nnz(self):
        """
        Combined number of nonzeros in L and U: L.nnz + U.nnz
        """
        return self._L.nnz + self._U.nnz
