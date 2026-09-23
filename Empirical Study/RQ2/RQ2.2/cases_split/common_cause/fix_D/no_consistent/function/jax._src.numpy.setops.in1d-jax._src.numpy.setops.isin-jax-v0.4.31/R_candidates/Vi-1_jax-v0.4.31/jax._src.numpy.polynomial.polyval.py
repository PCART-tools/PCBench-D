@partial(jit, static_argnames=['unroll'])
def polyval(p: ArrayLike, x: ArrayLike, *, unroll: int = 16) -> Array:
  r"""Evaluates the polynomial at specific values.

  JAX implementations of :func:`numpy.polyval`.

  For the 1D-polynomial coefficients ``p`` of length ``M``, the function returns
  the value:

  .. math::

    p_0 x^{M - 1} + p_1 x^{M - 2} + ... + p_{M - 1}

  Args:
    p: An array of polynomial coefficients of shape ``(M,)``.
    x: A number or an array of numbers.
    unroll: A number used to control the number of unrolled steps with
      ``lax.scan``. It must be specified statically.

  Returns:
    An array of same shape as ``x``.

  Note:

    The ``unroll`` parameter is JAX specific. It does not affect correctness but
    can have a major impact on performance for evaluating high-order polynomials.
    The parameter controls the number of unrolled steps with ``lax.scan`` inside
    the ``jnp.polyval`` implementation. Consider setting ``unroll=128`` (or even
    higher) to improve runtime performance on accelerators, at the cost of
    increased compilation time.

  See also:
    - :func:`jax.numpy.polyfit`: Least squares polynomial fit.
    - :func:`jax.numpy.poly`: Finds the coefficients of a polynomial with given
      roots.
    - :func:`jax.numpy.roots`: Computes the roots of a polynomial for given
      coefficients.

  Example:
    >>> p = jnp.array([2, 5, 1])
    >>> jnp.polyval(p, 3)
    Array(34., dtype=float32)

    If ``x`` is a 2D array, ``polyval`` returns 2D-array with same shape as
    that of ``x``:

    >>> x = jnp.array([[2, 1, 5],
    ...                [3, 4, 7],
    ...                [1, 3, 5]])
    >>> jnp.polyval(p, x)
    Array([[ 19.,   8.,  76.],
           [ 34.,  53., 134.],
           [  8.,  34.,  76.]], dtype=float32)
  """
  check_arraylike("polyval", p, x)
  p_arr, x_arr = promote_dtypes_inexact(p, x)
  del p, x
  shape = lax.broadcast_shapes(p_arr.shape[1:], x_arr.shape)
  y = lax.full_like(x_arr, 0, shape=shape, dtype=x_arr.dtype)
  y, _ = lax.scan(lambda y, p: (y * x_arr + p, None), y, p_arr, unroll=unroll)
  return y
