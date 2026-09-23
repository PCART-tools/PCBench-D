def lu(x: ArrayLike) -> tuple[Array, Array, Array]:
  """LU decomposition with partial pivoting.

  Computes the matrix decomposition:

  .. math::
    P.A = L.U

  where :math:`P` is a permutation of the rows of :math:`A`, :math:`L` is a
  lower-triangular matrix with unit-diagonal elements, and :math:`U` is an
  upper-triangular matrix.

  Args:
    x: A batch of matrices with shape ``[..., m, n]``.

  Returns:
    A tuple ``(lu, pivots, permutation)``.

    ``lu`` is a batch of matrices with the same shape and dtype as ``x``
    containing the :math:`L` matrix in its lower triangle and the :math:`U`
    matrix in its upper triangle. The (unit) diagonal elements of :math:`L` are
    not represented explicitly.

    ``pivots`` is an int32 array with shape ``[..., min(m, n)]`` representing a
    sequence of row swaps that should be performed on :math:`A`.

    ``permutation`` is an alternative representation of the sequence of row
    swaps as a permutation, represented as an int32 array with shape
    ``[..., m]``.
  """
  lu, pivots, permutation = lu_p.bind(x)
  return lu, pivots, permutation
