def bincount(x: ArrayLike, weights: ArrayLike | None = None,
             minlength: int = 0, *, length: int | None = None
             ) -> Array:
  """Count the number of occurrences of each value in an integer array.

  JAX implementation of :func:`numpy.bincount`.

  For an array of positive integers ``x``, this function returns an array ``counts``
  of size ``x.max() + 1``, such that ``counts[i]`` contains the number of occurrences
  of the value ``i`` in ``x``.

  The JAX version has a few differences from the NumPy version:

  - In NumPy, passing an array ``x`` with negative entries will result in an error.
    In JAX, negative values are clipped to zero.
  - JAX adds an optional ``length`` parameter which can be used to statically specify
    the length of the output array so that this function can be used with transformations
    like :func:`jax.jit`. In this case, items larger than `length + 1` will be dropped.

  Args:
    x : N-dimensional array of positive integers
    weights: optional array of weights associated with ``x``. If not specified, the
      weight for each entry will be ``1``.
    minlength: the minimum length of the output counts array.
    length: the length of the output counts array. Must be specified statically for
      ``bincount`` to be used with :func:`jax.jit` and other JAX transformations.

  Returns:
    An array of counts or summed weights reflecting the number of occurrences of values
    in ``x``.

  See Also:
    - :func:`jax.numpy.histogram`
    - :func:`jax.numpy.digitize`
    - :func:`jax.numpy.unique_counts`

  Examples:
    Basic bincount:

    >>> x = jnp.array([1, 1, 2, 3, 3, 3])
    >>> jnp.bincount(x)
    Array([0, 2, 1, 3], dtype=int32)

    Weighted bincount:

    >>> weights = jnp.array([1, 2, 3, 4, 5, 6])
    >>> jnp.bincount(x, weights)
    Array([ 0,  3,  3, 15], dtype=int32)

    Specifying a static ``length`` makes this jit-compatible:

    >>> jit_bincount = jax.jit(jnp.bincount, static_argnames=['length'])
    >>> jit_bincount(x, length=5)
    Array([0, 2, 1, 3, 0], dtype=int32)

    Any negative numbers are clipped to the first bin, and numbers beyond the
    specified ``length`` are dropped:

    >>> x = jnp.array([-1, -1, 1, 3, 10])
    >>> jnp.bincount(x, length=5)
    Array([2, 1, 0, 1, 0], dtype=int32)
  """
  util.check_arraylike("bincount", x)
  if not issubdtype(_dtype(x), integer):
    raise TypeError(f"x argument to bincount must have an integer type; got {_dtype(x)}")
  if ndim(x) != 1:
    raise ValueError("only 1-dimensional input supported.")
  minlength = core.concrete_or_error(operator.index, minlength,
      "The error occurred because of argument 'minlength' of jnp.bincount.")
  if length is None:
    x_arr = core.concrete_or_error(asarray, x,
      "The error occurred because of argument 'x' of jnp.bincount. "
      "To avoid this error, pass a static `length` argument.")
    length = max(minlength, x_arr.size and int(x_arr.max()) + 1)
  else:
    length = core.concrete_dim_or_error(length,
        "The error occurred because of argument 'length' of jnp.bincount.")
  if weights is None:
    weights = np.array(1, dtype=int_)
  elif shape(x) != shape(weights):
    raise ValueError("shape of weights must match shape of x.")
  return zeros(length, _dtype(weights)).at[clip(x, 0)].add(weights)
