def reshape(
    a: ArrayLike, shape: DimSize | Shape | None = None, order: str = "C", *,
    newshape: DimSize | Shape | DeprecatedArg = DeprecatedArg(),
    copy: bool | None = None) -> Array:
  """Return a reshaped copy of an array.

  JAX implementation of :func:`numpy.reshape`, implemented in terms of
  :func:`jax.lax.reshape`.

  Args:
    a: input array to reshape
    shape: integer or sequence of integers giving the new shape, which must match the
      size of the input array. If any single dimension is given size ``-1``, it will be
      replaced with a value such that the output has the correct size.
    order: ``'F'`` or ``'C'``, specifies whether the reshape should apply column-major
      (fortran-style, ``"F"``) or row-major (C-style, ``"C"``) order; default is ``"C"``.
      JAX does not support ``order="A"``.
    copy: unused by JAX; JAX always returns a copy, though under JIT the compiler
      may optimize such copies away.
    newshape: deprecated alias of the ``shape`` argument. Will result in a
      :class:`DeprecationWarning` if used.

  Returns:
    reshaped copy of input array with the specified shape.

  Notes:
    Unlike :func:`numpy.reshape`, :func:`jax.numpy.reshape` will return a copy rather
    than a view of the input array. However, under JIT, the compiler will optimize-away
    such copies when possible, so this doesn't have performance impacts in practice.

  See Also:
    - :meth:`jax.Array.reshape`: equivalent functionality via an array method.
    - :func:`jax.numpy.ravel`: flatten an array into a 1D shape.
    - :func:`jax.numpy.squeeze`: remove one or more length-1 axes from an array's shape.

  Examples:
    >>> x = jnp.array([[1, 2, 3],
    ...                [4, 5, 6]])
    >>> jnp.reshape(x, 6)
    Array([1, 2, 3, 4, 5, 6], dtype=int32)
    >>> jnp.reshape(x, (3, 2))
    Array([[1, 2],
           [3, 4],
           [5, 6]], dtype=int32)

    You can use ``-1`` to automatically compute a shape that is consistent with
    the input size:

    >>> jnp.reshape(x, -1)  # -1 is inferred to be 6
    Array([1, 2, 3, 4, 5, 6], dtype=int32)
    >>> jnp.reshape(x, (-1, 2))  # -1 is inferred to be 3
    Array([[1, 2],
           [3, 4],
           [5, 6]], dtype=int32)

    The default ordering of axes in the reshape is C-style row-major ordering.
    To use Fortran-style column-major ordering, specify ``order='F'``:

    >>> jnp.reshape(x, 6, order='F')
    Array([1, 4, 2, 5, 3, 6], dtype=int32)
    >>> jnp.reshape(x, (3, 2), order='F')
    Array([[1, 5],
           [4, 3],
           [2, 6]], dtype=int32)

    For convenience, this functionality is also available via the
    :meth:`jax.Array.reshape` method:

    >>> x.reshape(3, 2)
    Array([[1, 2],
           [3, 4],
           [5, 6]], dtype=int32)
  """
  del copy  # unused

  __tracebackhide__ = True
  util.check_arraylike("reshape", a)

  # TODO(micky774): deprecated 2024-5-9, remove after deprecation expires.
  if not isinstance(newshape, DeprecatedArg):
    if shape is not None:
      raise ValueError(
        "jnp.reshape received both `shape` and `newshape` arguments. Note that "
        "using `newshape` is deprecated, please only use `shape` instead."
      )
    deprecations.warn(
      "jax-numpy-reshape-newshape",
      ("The newshape argument of jax.numpy.reshape is deprecated. "
       "Please use the shape argument instead."), stacklevel=2)
    shape = newshape
    del newshape
  elif shape is None:
    raise TypeError(
      "jnp.shape requires passing a `shape` argument, but none was given."
    )
  try:
    # forward to method for ndarrays
    return a.reshape(shape, order=order)  # type: ignore[call-overload,union-attr]
  except AttributeError:
    pass
  return asarray(a).reshape(shape, order=order)
