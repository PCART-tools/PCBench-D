@jit
def polyadd(a1: ArrayLike, a2: ArrayLike) -> Array:
  r"""Returns the sum of the two polynomials.

  JAX implementation of :func:`numpy.polyadd`.

  Args:
    a1: Array of polynomial coefficients.
    a2: Array of polynomial coefficients.

  Returns:
    An array containing the coefficients of the sum of input polynomials.

  Note:
    :func:`jax.numpy.polyadd` only accepts arrays as input unlike
    :func:`numpy.polyadd` which accepts scalar inputs as well.

  See also:
    - :func:`jax.numpy.polysub`: Computes the difference of two polynomials.
    - :func:`jax.numpy.polymul`: Computes the product of two polynomials.
    - :func:`jax.numpy.polydiv`: Computes the quotient and remainder of polynomial
      division.

  Example:
    >>> x1 = jnp.array([2, 3])
    >>> x2 = jnp.array([5, 4, 1])
    >>> jnp.polyadd(x1, x2)
    Array([5, 6, 4], dtype=int32)

    >>> x3 = jnp.array([[2, 3, 1]])
    >>> x4 = jnp.array([[5, 7, 3],
    ...                 [8, 2, 6]])
    >>> jnp.polyadd(x3, x4)
    Array([[ 5,  7,  3],
           [10,  5,  7]], dtype=int32)

    >>> x5 = jnp.array([1, 3, 5])
    >>> x6 = jnp.array([[5, 7, 9],
    ...                 [8, 6, 4]])
    >>> jnp.polyadd(x5, x6)  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    ...
    ValueError: Cannot broadcast to shape with fewer dimensions: arr_shape=(2, 3) shape=(2,)
    >>> x7 = jnp.array([2])
    >>> jnp.polyadd(x6, x7)
    Array([[ 5,  7,  9],
           [10,  8,  6]], dtype=int32)
  """
  check_arraylike("polyadd", a1, a2)
  a1_arr, a2_arr = promote_dtypes(a1, a2)
  del a1, a2
  if a2_arr.shape[0] <= a1_arr.shape[0]:
    return a1_arr.at[-a2_arr.shape[0]:].add(a2_arr)
  else:
    return a2_arr.at[-a1_arr.shape[0]:].add(a1_arr)
