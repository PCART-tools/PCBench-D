@partial(jit, static_argnames=('deg', 'rcond', 'full', 'cov'))
def polyfit(x: ArrayLike, y: ArrayLike, deg: int, rcond: float | None = None,
            full: bool = False, w: ArrayLike | None = None, cov: bool = False
            ) -> Array | tuple[Array, ...]:
  r"""Least squares polynomial fit to data.

  Jax implementation of :func:`numpy.polyfit`.

  Given a set of data points ``(x, y)`` and degree of polynomial ``deg``, the
  function finds a polynomial equation of the form:

  .. math::

	   y = p(x) = p[0] x^{deg} + p[1] x^{deg - 1} + ... + p[deg]

  Args:
    x: Array of data points of shape ``(M,)``.
    y: Array of data points of shape ``(M,)`` or ``(M, K)``.
    deg: Degree of the polynomials. It must be specified statically.
    rcond: Relative condition number of the fit. Default value is ``len(x) * eps``.
       It must be specified statically.
    full: Switch that controls the return value. Default is ``False`` which
      restricts the return value to the array of polynomail coefficients ``p``.
      If ``True``, the function returns a tuple ``(p, resids, rank, s, rcond)``.
      It must be specified statically.
    w: Array of weights of shape ``(M,)``. If None, all data points are considered
      to have equal weight. If not None, the weight :math:`w_i` is applied to the
      unsquared residual of :math:`y_i - \widehat{y}_i` at :math:`x_i`, where
      :math:`\widehat{y}_i` is the fitted value of :math:`y_i`. Default is None.
    cov: Boolean or string. If ``True``, returns the covariance matrix scaled
      by ``resids/(M-deg-1)`` along with ploynomial coefficients. If
      ``cov='unscaled'``, returns the unscaaled version of covariance matrix.
      Default is ``False``. ``cov`` is ignored if ``full=True``. It must be
      specified statically.

  Returns:
    - An array polynomial coefficients ``p`` if ``full=False`` and ``cov=False``.

    - A tuple of arrays ``(p, resids, rank, s, rcond)`` if ``full=True``. Where

      - ``p`` is an array of shape ``(M,)`` or ``(M, K)`` containing the polynomial
        coefficients.
      - ``resids`` is the sum of squared residual of shape () or (K,).
      - ``rank`` is the rank of the matrix ``x``.
      - ``s`` is the singular values of the matrix ``x``.
      - ``rcond`` as the array.
    - A tuple of arrays ``(p, C)`` if ``full=False`` and ``cov=True``. Where

      - ``p`` is an array of shape ``(M,)`` or ``(M, K)`` containing the polynomial
        coefficients.
      - ``C`` is the covariance matrix of polynomial coefficients of shape
        ``(deg + 1, deg + 1)`` or ``(deg + 1, deg + 1, 1)``.

  Note:
    Unlike :func:`numpy.polyfit` implementation of polyfit, :func:`jax.numpy.polyfit`
    will not warn on rank reduction, which indicates an ill conditioned matrix.

  See Also:
    - :func:`jax.numpy.poly`: Finds the polynomial coefficients of the given
      sequence of roots.
    - :func:`jax.numpy.polyval`: Evaluate a polynomial at specific values.
    - :func:`jax.numpy.roots`: Computes the roots of a polynomial for given
      coefficients.

  Examples:
    >>> x = jnp.array([3., 6., 9., 4.])
    >>> y = jnp.array([[0, 1, 2],
    ...                [2, 5, 7],
    ...                [8, 4, 9],
    ...                [1, 6, 3]])
    >>> p = jnp.polyfit(x, y, 2)
    >>> with jnp.printoptions(precision=2, suppress=True):
    ...   print(p)
    [[ 0.2  -0.35 -0.14]
     [-1.17  4.47  2.96]
     [ 1.95 -8.21 -5.93]]

    If ``full=True``, returns a tuple of arrays as follows:

    >>> p, resids, rank, s, rcond = jnp.polyfit(x, y, 2, full=True)
    >>> with jnp.printoptions(precision=2, suppress=True):
    ...   print("Polynomial Coefficients:", "\n", p, "\n",
    ...         "Residuals:", resids, "\n",
    ...         "Rank:", rank, "\n",
    ...         "s:", s, "\n",
    ...         "rcond:", rcond)
    Polynomial Coefficients:
    [[ 0.2  -0.35 -0.14]
    [-1.17  4.47  2.96]
    [ 1.95 -8.21 -5.93]]
    Residuals: [0.37 5.94 0.61]
    Rank: 3
    s: [1.67 0.47 0.04]
    rcond: 4.7683716e-07

    If ``cov=True`` and ``full=False``, returns a tuple of arrays having
    polynomial coefficients and covariance matrix.

    >>> p, C = jnp.polyfit(x, y, 2, cov=True)
    >>> p.shape, C.shape
    ((3, 3), (3, 3, 1))
  """
  if w is None:
    check_arraylike("polyfit", x, y)
  else:
    check_arraylike("polyfit", x, y, w)
  deg = core.concrete_or_error(int, deg, "deg must be int")
  order = deg + 1
  # check arguments
  x_arr, y_arr = asarray(x), asarray(y)
  del x, y
  if deg < 0:
    raise ValueError("expected deg >= 0")
  if x_arr.ndim != 1:
    raise TypeError("expected 1D vector for x")
  if x_arr.size == 0:
    raise TypeError("expected non-empty vector for x")
  if y_arr.ndim < 1 or y_arr.ndim > 2:
    raise TypeError("expected 1D or 2D array for y")
  if x_arr.shape[0] != y_arr.shape[0]:
    raise TypeError("expected x and y to have same length")

  # set rcond
  if rcond is None:
    rcond = len(x_arr) * finfo(x_arr.dtype).eps
  rcond = core.concrete_or_error(float, rcond, "rcond must be float")
  # set up least squares equation for powers of x
  lhs = vander(x_arr, order)
  rhs = y_arr

  # apply weighting
  if w is not None:
    w, = promote_dtypes_inexact(w)
    w_arr = asarray(w)
    if w_arr.ndim != 1:
      raise TypeError("expected a 1-d array for weights")
    if w_arr.shape[0] != y_arr.shape[0]:
      raise TypeError("expected w and y to have the same length")
    lhs *= w_arr[:, np.newaxis]
    if rhs.ndim == 2:
      rhs *= w_arr[:, np.newaxis]
    else:
      rhs *= w_arr

  # scale lhs to improve condition number and solve
  scale = sqrt((lhs*lhs).sum(axis=0))
  lhs /= scale[np.newaxis,:]
  c, resids, rank, s = linalg.lstsq(lhs, rhs, rcond)
  c = (c.T/scale).T  # broadcast scale coefficients

  if full:
    return c, resids, rank, s, asarray(rcond)
  elif cov:
    Vbase = linalg.inv(dot(lhs.T, lhs))
    Vbase /= outer(scale, scale)
    if cov == "unscaled":
      fac = 1
    else:
      if len(x_arr) <= order:
        raise ValueError("the number of data points must exceed order "
                            "to scale the covariance matrix")
      fac = resids / (len(x_arr) - order)
      fac = fac[0] #making np.array() of shape (1,) to int
    if y_arr.ndim == 1:
      return c, Vbase * fac
    else:
      return c, Vbase[:, :, np.newaxis] * fac
  else:
    return c
