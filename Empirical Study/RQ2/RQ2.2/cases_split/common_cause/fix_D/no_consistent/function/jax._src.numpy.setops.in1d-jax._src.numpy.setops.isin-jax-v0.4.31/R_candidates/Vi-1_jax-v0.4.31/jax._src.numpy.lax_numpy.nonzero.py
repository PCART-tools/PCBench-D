def nonzero(a: ArrayLike, *, size: int | None = None,
            fill_value: None | ArrayLike | tuple[ArrayLike, ...] = None
    ) -> tuple[Array, ...]:
  """Return indices of nonzero elements of an array.

  JAX implementation of :func:`numpy.nonzero`.

  Because the size of the output of ``nonzero`` is data-dependent, the function
  is not compatible with JIT and other transformations. The JAX version adds
  the optional ``size`` argument which must be specified statically for
  ``jnp.nonzero`` to be used within JAX's transformations.

  Args:
    a: N-dimensional array.
    size: optional static integer specifying the number of nonzero entries to
      return. If there are more nonzero elements than the specified ``size``,
      then indices will be truncated at the end. If there are fewer nonzero
      elements than the specified size, then indices will be padded with
      ``fill_value``, which defaults to zero.
    fill_value: optional padding value when ``size`` is specified. Defaults to 0.

  Returns:
    Tuple of JAX Arrays of length ``a.ndim``, containing the indices of each
    nonzero value.

  See also:
    - :func:`jax.numpy.flatnonzero`
    - :func:`jax.numpy.where`

  Examples:

    One-dimensional array returns a length-1 tuple of indices:

    >>> x = jnp.array([0, 5, 0, 6, 0, 7])
    >>> jnp.nonzero(x)
    (Array([1, 3, 5], dtype=int32),)

    Two-dimensional array returns a length-2 tuple of indices:

    >>> x = jnp.array([[0, 5, 0],
    ...                [6, 0, 7]])
    >>> jnp.nonzero(x)
    (Array([0, 1, 1], dtype=int32), Array([1, 0, 2], dtype=int32))

    In either case, the resulting tuple of indices can be used directly to extract
    the nonzero values:

    >>> indices = jnp.nonzero(x)
    >>> x[indices]
    Array([5, 6, 7], dtype=int32)

    The output of ``nonzero`` has a dynamic shape, because the number of returned
    indices depends on the contents of the input array. As such, it is incompatible
    with JIT and other JAX transformations:

    >>> x = jnp.array([0, 5, 0, 6, 0, 7])
    >>> jax.jit(jnp.nonzero)(x)  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
      ...
    ConcretizationTypeError: Abstract tracer value encountered where concrete value is expected: traced array with shape int32[].
    The size argument of jnp.nonzero must be statically specified to use jnp.nonzero within JAX transformations.

    This can be addressed by passing a static ``size`` parameter to specify the
    desired output shape:

    >>> nonzero_jit = jax.jit(jnp.nonzero, static_argnames='size')
    >>> nonzero_jit(x, size=3)
    (Array([1, 3, 5], dtype=int32),)

    If ``size`` does not match the true size, the result will be either truncated or padded:

    >>> nonzero_jit(x, size=2)  # size < 3: indices are truncated
    (Array([1, 3], dtype=int32),)
    >>> nonzero_jit(x, size=5)  # size > 3: indices are padded with zeros.
    (Array([1, 3, 5, 0, 0], dtype=int32),)

    You can specify a custom fill value for the padding using the ``fill_value`` argument:

    >>> nonzero_jit(x, size=5, fill_value=len(x))
    (Array([1, 3, 5, 6, 6], dtype=int32),)
  """
  util.check_arraylike("nonzero", a)
  arr = asarray(a)
  del a
  if ndim(arr) == 0:
    raise ValueError("Calling nonzero on 0d arrays is not allowed. "
                     "Use jnp.atleast_1d(scalar).nonzero() instead.")
  mask = arr if arr.dtype == bool else (arr != 0)
  calculated_size_ = mask.sum() if size is None else size
  calculated_size: int = core.concrete_dim_or_error(calculated_size_,
    "The size argument of jnp.nonzero must be statically specified "
    "to use jnp.nonzero within JAX transformations.")
  if arr.size == 0 or calculated_size == 0:
    return tuple(zeros(calculated_size, int) for dim in arr.shape)
  flat_indices = reductions.cumsum(
      bincount(reductions.cumsum(mask), length=calculated_size))
  strides: np.ndarray = (np.cumprod(arr.shape[::-1])[::-1] // arr.shape).astype(int_)
  out = tuple((flat_indices // stride) % size for stride, size in zip(strides, arr.shape))
  if fill_value is not None:
    fill_value_tup = fill_value if isinstance(fill_value, tuple) else arr.ndim * (fill_value,)
    if any(_shape(val) != () for val in fill_value_tup):
      raise ValueError(f"fill_value must be a scalar or a tuple of length {arr.ndim}; got {fill_value}")
    fill_mask = arange(calculated_size) >= mask.sum()
    out = tuple(where(fill_mask, fval, entry) for fval, entry in safe_zip(fill_value_tup, out))
  return out
