@partial(jit, static_argnames=('side', 'method'))
@jax.default_matmul_precision("float32")
def polar(a: ArrayLike, side: str = 'right', *, method: str = 'qdwh', eps: Optional[float] = None,
          max_iterations: Optional[int] = None) -> tuple[Array, Array]:
  r"""Computes the polar decomposition.

  Given the :math:`m \times n` matrix :math:`a`, returns the factors of the polar
  decomposition :math:`u` (also :math:`m \times n`) and :math:`p` such that
  :math:`a = up` (if side is ``"right"``; :math:`p` is :math:`n \times n`) or
  :math:`a = pu` (if side is ``"left"``; :math:`p` is :math:`m \times m`),
  where :math:`p` is positive semidefinite.  If :math:`a` is nonsingular,
  :math:`p` is positive definite and the
  decomposition is unique. :math:`u` has orthonormal columns unless
  :math:`n > m`, in which case it has orthonormal rows.

  Writing the SVD of :math:`a` as
  :math:`a = u_\mathit{svd} \cdot s_\mathit{svd} \cdot v^h_\mathit{svd}`, we
  have :math:`u = u_\mathit{svd} \cdot v^h_\mathit{svd}`. Thus the unitary
  factor :math:`u` can be constructed as the application of the sign function to
  the singular values of :math:`a`; or, if :math:`a` is Hermitian, the
  eigenvalues.

  Several methods exist to compute the polar decomposition. Currently two
  are supported:

  * ``method="svd"``:

    Computes the SVD of :math:`a` and then forms
    :math:`u = u_\mathit{svd} \cdot v^h_\mathit{svd}`.

  * ``method="qdwh"``:

    Applies the `QDWH`_ (QR-based Dynamically Weighted Halley) algorithm.

  Args:
    a: The :math:`m \times n` input matrix.
    side: Determines whether a right or left polar decomposition is computed.
      If ``side`` is ``"right"`` then :math:`a = up`. If ``side`` is ``"left"``
      then :math:`a = pu`. The default is ``"right"``.
    method: Determines the algorithm used, as described above.
    precision: :class:`~jax.lax.Precision` object specifying the matmul precision.
    eps: The final result will satisfy
      :math:`\left|x_k - x_{k-1}\right| < \left|x_k\right| (4\epsilon)^{\frac{1}{3}}`,
      where :math:`x_k` are the QDWH iterates. Ignored if ``method`` is not
      ``"qdwh"``.
    max_iterations: Iterations will terminate after this many steps even if the
      above is unsatisfied.  Ignored if ``method`` is not ``"qdwh"``.

  Returns:
    A ``(unitary, posdef)`` tuple, where ``unitary`` is the unitary factor
    (:math:`m \times n`), and ``posdef`` is the positive-semidefinite factor.
    ``posdef`` is either :math:`n \times n` or :math:`m \times m` depending on
    whether ``side`` is ``"right"`` or ``"left"``, respectively.

  .. _QDWH: https://epubs.siam.org/doi/abs/10.1137/090774999
  """
  arr = jnp.asarray(a)
  if arr.ndim != 2:
    raise ValueError("The input `a` must be a 2-D array.")

  if side not in ["right", "left"]:
    raise ValueError("The argument `side` must be either 'right' or 'left'.")

  m, n = arr.shape
  if method == "qdwh":
    # TODO(phawkins): return info also if the user opts in?
    if m >= n and side == "right":
      unitary, posdef, _, _ = qdwh.qdwh(arr, is_hermitian=False, eps=eps)
    elif m < n and side == "left":
      arr = arr.T.conj()
      unitary, posdef, _, _ = qdwh.qdwh(arr, is_hermitian=False, eps=eps)
      posdef = posdef.T.conj()
      unitary = unitary.T.conj()
    else:
      raise NotImplementedError("method='qdwh' only supports mxn matrices "
                                "where m < n where side='right' and m >= n "
                                f"side='left', got {arr.shape} with {side=}")
  elif method == "svd":
    u_svd, s_svd, vh_svd = lax_linalg.svd(arr, full_matrices=False)
    s_svd = s_svd.astype(u_svd.dtype)
    unitary = u_svd @ vh_svd
    if side == "right":
      # a = u * p
      posdef = (vh_svd.T.conj() * s_svd[None, :]) @ vh_svd
    else:
      # a = p * u
      posdef = (u_svd * s_svd[None, :]) @ (u_svd.T.conj())
  else:
    raise ValueError(f"Unknown polar decomposition method {method}.")

  return unitary, posdef
