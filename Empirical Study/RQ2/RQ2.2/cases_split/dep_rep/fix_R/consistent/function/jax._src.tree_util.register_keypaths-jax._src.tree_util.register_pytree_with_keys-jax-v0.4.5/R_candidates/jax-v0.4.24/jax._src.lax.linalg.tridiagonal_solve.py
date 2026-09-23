def tridiagonal_solve(dl: Array, d: Array, du: Array, b: Array) -> Array:
  r"""Computes the solution of a tridiagonal linear system.

  This function computes the solution of a tridiagonal linear system:

  .. math::
    A . X = B

  Args:

    dl: A batch of vectors with shape ``[..., m]``.
      The lower diagonal of A: ``dl[i] := A[i, i-1]`` for i in ``[0,m)``.
      Note that ``dl[0] = 0``.
    d: A batch of vectors with shape ``[..., m]``.
      The middle diagonal of A: ``d[i]  := A[i, i]`` for i in ``[0,m)``.
    du: A batch of vectors with shape ``[..., m]``.
      The upper diagonal of A: ``du[i] := A[i, i+1]`` for i in ``[0,m)``.
      Note that ``dl[m - 1] = 0``.
    b: Right hand side matrix.

  Returns:
    Solution ``X`` of tridiagonal system.
  """
  if dl.shape != d.shape or d.shape != du.shape:
    raise ValueError(
        f'dl={dl.shape}, d={d.shape} and du={du.shape} must all be `[m]`')

  m = dl.shape[-1]
  if m < 3:
    raise ValueError(f'm ({m}) must be >= 3')

  ldb = b.shape[-2]
  n = b.shape[-1]
  if ldb < max(1, m):
    raise ValueError(f'Leading dimension of b={ldb} must be ≥ max(1, {m})')

  if dl.dtype != d.dtype or d.dtype != du.dtype or du.dtype != b.dtype:
    raise ValueError(f'dl={dl.dtype}, d={d.dtype}, du={du.dtype} and '
                     f'b={b.dtype} must be the same dtype,')

  t = dl.dtype
  if t not in (np.float32, np.float64):
    raise ValueError(f'Only f32/f64 are supported, got {t}')

  return tridiagonal_solve_p.bind(dl, d, du, b, m=m, n=n, ldb=ldb, t=t)
