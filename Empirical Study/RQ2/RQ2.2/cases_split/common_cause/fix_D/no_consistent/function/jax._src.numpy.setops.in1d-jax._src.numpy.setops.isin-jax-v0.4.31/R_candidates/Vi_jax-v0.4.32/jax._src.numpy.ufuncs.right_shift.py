@partial(jit, inline=True)
def right_shift(x1: ArrayLike, x2: ArrayLike, /) -> Array:
  r"""Right shift the bits of ``x1`` to the amount specified in ``x2``.

  JAX implementation of :obj:`numpy.right_shift`.

  Args:
    x1: Input array, only accepts unsigned integer subtypes
    x2: The amount of bits to shift each element in ``x1`` to the right, only accepts
      integer subtypes

  Returns:
    An array-like object containing the right shifted elements of ``x1`` by the
    amount specified in ``x2``, with the same shape as the broadcasted shape of
    ``x1`` and ``x2``.

  Note:
    If ``x1.shape != x2.shape``, they must be compatible for broadcasting to a
    shared shape, this shared shape will also be the shape of the output. Right shifting
    a scalar x1 by scalar x2 is equivalent to ``x1 // 2**x2``.

  Examples:
    >>> def print_binary(x):
    ...   return [bin(int(val)) for val in x]

    >>> x1 = jnp.array([1, 2, 4, 8])
    >>> print_binary(x1)
    ['0b1', '0b10', '0b100', '0b1000']
    >>> x2 = 1
    >>> result = jnp.right_shift(x1, x2)
    >>> result
    Array([0, 1, 2, 4], dtype=int32)
    >>> print_binary(result)
    ['0b0', '0b1', '0b10', '0b100']

    >>> x1 = 16
    >>> print_binary([x1])
    ['0b10000']
    >>> x2 = jnp.array([1, 2, 3, 4])
    >>> result = jnp.right_shift(x1, x2)
    >>> result
    Array([8, 4, 2, 1], dtype=int32)
    >>> print_binary(result)
    ['0b1000', '0b100', '0b10', '0b1']
  """
  x1, x2 = promote_args_numeric(np.right_shift.__name__, x1, x2)
  lax_fn = lax.shift_right_logical if \
    np.issubdtype(x1.dtype, np.unsignedinteger) else lax.shift_right_arithmetic
  return lax_fn(x1, x2)
