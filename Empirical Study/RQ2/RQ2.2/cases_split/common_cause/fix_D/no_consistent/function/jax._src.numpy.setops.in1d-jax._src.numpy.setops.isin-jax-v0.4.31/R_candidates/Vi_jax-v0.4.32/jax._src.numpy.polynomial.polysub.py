@jit
def polysub(a1: ArrayLike, a2: ArrayLike) -> Array:
  r"""Returns the difference of two polynomials.

  JAX implementation of :func:`numpy.polysub`.

  Args:
    a1: Array of minuend polynomial coefficients.
    a2: Array of subtrahend polynomial coefficients.

  Returns:
    An array containing the coefficients of the difference of two polynomials.

  Note:
    :func:`jax.numpy.polysub` only accepts arrays as input unlike
    :func:`numpy.polysub` which accepts scalar inputs as well.

  See also:
    - :func:`jax.numpy.polyadd`: Computes the sum of two polynomials.
    - :func:`jax.numpy.polymul`: Computes the product of two polynomials.
    - :func:`jax.numpy.polydiv`: Computes the quotient and remainder of polynomial
      division.

  Example:
    >>> x1 = jnp.array([2, 3])
    >>> x2 = jnp.array([5, 4, 1])
    >>> jnp.polysub(x1, x2)
    Array([-5, -2,  2], dtype=int32)

    >>> x3 = jnp.array([[2, 3, 1]])
    >>> x4 = jnp.array([[5, 7, 3],
    ...                 [8, 2, 6]])
    >>> jnp.polysub(x3, x4)
    Array([[-5, -7, -3],
           [-6,  1, -5]], dtype=int32)

    >>> x5 = jnp.array([1, 3, 5])
    >>> x6 = jnp.array([[5, 7, 9],
    ...                 [8, 6, 4]])
    >>> jnp.polysub(x5, x6)  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    ...
    ValueError: Cannot broadcast to shape with fewer dimensions: arr_shape=(2, 3) shape=(2,)
    >>> x7 = jnp.array([2])
    >>> jnp.polysub(x6, x7)
    Array([[5, 7, 9],
           [6, 4, 2]], dtype=int32)
  """
  check_arraylike("polysub", a1, a2)
  a1, a2 = promote_dtypes(a1, a2)
  return polyadd(a1, -a2)
