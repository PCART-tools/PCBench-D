@partial(api.jit, static_argnames=('axis', 'keepdims'))
def count_nonzero(a: ArrayLike, axis: Axis = None,
                  keepdims: bool = False) -> Array:
  r"""Return the number of nonzero elements along a given axis.

  JAX implementation of :func:`numpy.count_nonzero`.

  Args:
    a: input array.
    axis: optional, int or sequence of ints, default=None. Axis along which the
      number of nonzeros are counted. If None, counts within the flattened array.
    keepdims: bool, default=False. If true, reduced axes are left in the result
      with size 1.

  Returns:
    An array with number of nonzeros elements along specified axis of the input.

  Examples:
    By default, ``jnp.count_nonzero`` counts the nonzero values along all axes.

    >>> x = jnp.array([[1, 0, 0, 0],
    ...                [0, 0, 1, 0],
    ...                [1, 1, 1, 0]])
    >>> jnp.count_nonzero(x)
    Array(5, dtype=int32)

    If ``axis=1``, counts along axis 1.

    >>> jnp.count_nonzero(x, axis=1)
    Array([1, 1, 3], dtype=int32)

    To preserve the dimensions of input, you can set ``keepdims=True``.

    >>> jnp.count_nonzero(x, axis=1, keepdims=True)
    Array([[1],
           [1],
           [3]], dtype=int32)
  """
  check_arraylike("count_nonzero", a)
  return sum(lax.ne(a, _lax_const(a, 0)), axis=axis,
             dtype=dtypes.canonicalize_dtype(int), keepdims=keepdims)
