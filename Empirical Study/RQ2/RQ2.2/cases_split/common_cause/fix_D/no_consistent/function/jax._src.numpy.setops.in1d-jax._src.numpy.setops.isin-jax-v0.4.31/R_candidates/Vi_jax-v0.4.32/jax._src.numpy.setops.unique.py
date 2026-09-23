def unique(ar: ArrayLike, return_index: bool = False, return_inverse: bool = False,
           return_counts: bool = False, axis: int | None = None,
           *, equal_nan: bool = True, size: int | None = None, fill_value: ArrayLike | None = None):
  """Return the unique values from an array.

  JAX implementation of :func:`numpy.unique`.

  Because the size of the output of ``unique`` is data-dependent, the function
  is not typically compatible with :func:`~jax.jit` and other JAX transformations.
  The JAX version adds the optional ``size`` argument which must be specified
  statically for ``jnp.unique`` to be used in such contexts.

  Args:
    ar: N-dimensional array from which unique values will be extracted.
    return_index: if True, also return the indices in ``ar`` where each value occurs
    return_inverse: if True, also return the indices that can be used to reconstruct
      ``ar`` from the unique values.
    return_counts: if True, also return the number of occurrences of each unique value.
    axis: if specified, compute unique values along the specified axis. If None (default),
      then flatten ``ar`` before computing the unique values.
    equal_nan: if True, consider NaN values equivalent when determining uniqueness.
    size: if specified, return only the first ``size`` sorted unique elements. If there are fewer
      unique elements than ``size`` indicates, the return value will be padded with ``fill_value``.
    fill_value: when ``size`` is specified and there are fewer than the indicated number of
      elements, fill the remaining entries ``fill_value``. Defaults to the minimum unique value.

  Returns:
    An array or tuple of arrays, depending on the values of ``return_index``, ``return_inverse``,
    and ``return_counts``. Returned values are

    - ``unique_values``:
        if ``axis`` is None, a 1D array of length ``n_unique``, If ``axis`` is
        specified, shape is ``(*ar.shape[:axis], n_unique, *ar.shape[axis + 1:])``.
    - ``unique_index``:
        *(returned only if return_index is True)* An array of shape ``(n_unique,)``. Contains
        the indices of the first occurrence of each unique value in ``ar``. For 1D inputs,
        ``ar[unique_index]`` is equivalent to ``unique_values``.
    - ``unique_inverse``:
        *(returned only if return_inverse is True)* An array of shape ``(ar.size,)`` if ``axis``
        is None, or of shape ``(ar.shape[axis],)`` if ``axis`` is specified.
        Contains the indices within ``unique_values`` of each value in ``ar``. For 1D inputs,
        ``unique_values[unique_inverse]`` is equivalent to ``ar``.
    - ``unique_counts``:
        *(returned only if return_counts is True)* An array of shape ``(n_unique,)``.
        Contains the number of occurrences of each unique value in ``ar``.

  See also:
    - :func:`jax.numpy.unique_counts`: shortcut to ``unique(arr, return_counts=True)``.
    - :func:`jax.numpy.unique_inverse`: shortcut to ``unique(arr, return_inverse=True)``.
    - :func:`jax.numpy.unique_all`: shortcut to ``unique`` with all return values.
    - :func:`jax.numpy.unique_values`: like ``unique``, but no optional return values.

  Examples:
    >>> x = jnp.array([3, 4, 1, 3, 1])
    >>> jnp.unique(x)
    Array([1, 3, 4], dtype=int32)

    **JIT compilation & the size argument**

    If you try this under :func:`~jax.jit` or another transformation, you will get an
    error because the output shape is dynamic:

    >>> jax.jit(jnp.unique)(x)  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
       ...
    jax.errors.ConcretizationTypeError: Abstract tracer value encountered where concrete value is expected: traced array with shape int32[5].
    The error arose for the first argument of jnp.unique(). To make jnp.unique() compatible with JIT and other transforms, you can specify a concrete value for the size argument, which will determine the output size.

    The issue is that the output of transformed functions must have static shapes.
    In order to make this work, you can pass a static ``size`` parameter:

    >>> jit_unique = jax.jit(jnp.unique, static_argnames=['size'])
    >>> jit_unique(x, size=3)
    Array([1, 3, 4], dtype=int32)

    If your static size is smaller than the true number of unique values, they will be truncated.

    >>> jit_unique(x, size=2)
    Array([1, 3], dtype=int32)

    If the static size is larger than the true number of unique values, they will be padded with
    ``fill_value``, which defaults to the minimum unique value:

    >>> jit_unique(x, size=5)
    Array([1, 3, 4, 1, 1], dtype=int32)
    >>> jit_unique(x, size=5, fill_value=0)
    Array([1, 3, 4, 0, 0], dtype=int32)

    **Multi-dimensional unique values**

    If you pass a multi-dimensional array to ``unique``, it will be flattened by default:

    >>> M = jnp.array([[1, 2],
    ...                [2, 3],
    ...                [1, 2]])
    >>> jnp.unique(M)
    Array([1, 2, 3], dtype=int32)

    If you pass an ``axis`` keyword, you can find unique *slices* of the array along
    that axis:

    >>> jnp.unique(M, axis=0)
    Array([[1, 2],
           [2, 3]], dtype=int32)

    **Returning indices**

    If you set ``return_index=True``, then ``unique`` returns the indices of the
    first occurrence of each unique value:

    >>> x = jnp.array([3, 4, 1, 3, 1])
    >>> values, indices = jnp.unique(x, return_index=True)
    >>> print(values)
    [1 3 4]
    >>> print(indices)
    [2 0 1]
    >>> jnp.all(values == x[indices])
    Array(True, dtype=bool)

    In multiple dimensions, the unique values can be extracted with :func:`jax.numpy.take`
    evaluated along the specified axis:

    >>> values, indices = jnp.unique(M, axis=0, return_index=True)
    >>> jnp.all(values == jnp.take(M, indices, axis=0))
    Array(True, dtype=bool)

    **Returning inverse**

    If you set ``return_inverse=True``, then ``unique`` returns the indices within the
    unique values for every entry in the input array:

    >>> x = jnp.array([3, 4, 1, 3, 1])
    >>> values, inverse = jnp.unique(x, return_inverse=True)
    >>> print(values)
    [1 3 4]
    >>> print(inverse)
    [1 2 0 1 0]
    >>> jnp.all(values[inverse] == x)
    Array(True, dtype=bool)

    In multiple dimensions, the input can be reconstructed using
    :func:`jax.numpy.take`:

    >>> values, inverse = jnp.unique(M, axis=0, return_inverse=True)
    >>> jnp.all(jnp.take(values, inverse, axis=0) == M)
    Array(True, dtype=bool)

    **Returning counts**

    If you set ``return_counts=True``, then ``unique`` returns the number of occurrences
    within the input for every unique value:

    >>> x = jnp.array([3, 4, 1, 3, 1])
    >>> values, counts = jnp.unique(x, return_counts=True)
    >>> print(values)
    [1 3 4]
    >>> print(counts)
    [2 2 1]

    For multi-dimensional arrays, this also returns a 1D array of counts
    indicating number of occurrences along the specified axis:

    >>> values, counts = jnp.unique(M, axis=0, return_counts=True)
    >>> print(values)
    [[1 2]
     [2 3]]
    >>> print(counts)
    [2 1]
  """
  check_arraylike("unique", ar)
  if size is None:
    ar = core.concrete_or_error(None, ar,
        "The error arose for the first argument of jnp.unique(). " + UNIQUE_SIZE_HINT)
  else:
    size = core.concrete_or_error(operator.index, size,
         "The error arose for the size argument of jnp.unique(). " + UNIQUE_SIZE_HINT)
  arr = asarray(ar)
  arr_shape = arr.shape
  if axis is None:
    axis_int: int = 0
    arr = arr.flatten()
  else:
    axis_int = canonicalize_axis(axis, arr.ndim)
  result = _unique(arr, axis_int, return_index, return_inverse, return_counts,
                   equal_nan=equal_nan, size=size, fill_value=fill_value)
  if return_inverse and axis is None:
    idx = 2 if return_index else 1
    result = (*result[:idx], result[idx].reshape(arr_shape), *result[idx + 1:])
  return result
