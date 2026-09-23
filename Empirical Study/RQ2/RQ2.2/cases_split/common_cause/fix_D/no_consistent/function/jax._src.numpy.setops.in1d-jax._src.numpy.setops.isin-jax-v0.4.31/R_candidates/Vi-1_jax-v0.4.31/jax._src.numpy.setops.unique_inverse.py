def unique_inverse(x: ArrayLike, /, *, size: int | None = None,
                   fill_value: ArrayLike | None = None) -> _UniqueInverseResult:
  """Return unique values from x, along with indices, inverse indices, and counts.

  JAX implementation of :func:`numpy.unique_inverse`; this is equivalent to calling
  :func:`jax.numpy.unique` with `return_inverse` and `equal_nan` set to True.

  Because the size of the output of ``unique_inverse`` is data-dependent, the function
  semantics are not typically compatible with :func:`~jax.jit` and other JAX
  transformations. The JAX version adds the optional ``size`` argument which
  must be specified statically for ``jnp.unique`` to be used in such contexts.

  Args:
    x: N-dimensional array from which unique values will be extracted.
    size: if specified, return only the first ``size`` sorted unique elements. If there are fewer
      unique elements than ``size`` indicates, the return value will be padded with ``fill_value``.
    fill_value: when ``size`` is specified and there are fewer than the indicated number of
      elements, fill the remaining entries ``fill_value``. Defaults to the minimum unique value.

  Returns:
    A tuple ``(values, indices, inverse_indices, counts)``, with the following properties:

    - ``values``:
        an array of shape ``(n_unique,)`` containing the unique values from ``x``.
    - ``inverse_indices``:
        An array of shape ``x.shape``. Contains the indices within ``values`` of each value
        in ``x``. For 1D inputs, ``values[inverse_indices]`` is equivalent to ``x``.

  See also:
    - :func:`jax.numpy.unique`: general function for computing unique values.
    - :func:`jax.numpy.unique_values`: compute only ``values``.
    - :func:`jax.numpy.unique_counts`: compute only ``values`` and ``counts``.
    - :func:`jax.numpy.unique_all`: compute ``values``, ``indices``, ``inverse_indices``,
      and ``counts``.

  Examples:
    Here we compute the unique values in a 1D array:

    >>> x = jnp.array([3, 4, 1, 3, 1])
    >>> result = jnp.unique_inverse(x)

    The result is a :class:`~typing.NamedTuple` with two named attributes.
    The ``values`` attribute contains the unique values from the array:

    >>> result.values
    Array([1, 3, 4], dtype=int32)

    The ``indices`` attribute contains the indices of the unique ``values`` within
    the input array:

    The ``inverse_indices`` attribute contains the indices of the input within ``values``:

    >>> result.inverse_indices
    Array([1, 2, 0, 1, 0], dtype=int32)
    >>> jnp.all(x == result.values[result.inverse_indices])
    Array(True, dtype=bool)

    For examples of the ``size`` and ``fill_value`` arguments, see :func:`jax.numpy.unique`.
  """
  check_arraylike("unique_inverse", x)
  values, inverse_indices = unique(x, return_inverse=True, equal_nan=False,
                                   size=size, fill_value=fill_value)
  return _UniqueInverseResult(values=values, inverse_indices=inverse_indices)
