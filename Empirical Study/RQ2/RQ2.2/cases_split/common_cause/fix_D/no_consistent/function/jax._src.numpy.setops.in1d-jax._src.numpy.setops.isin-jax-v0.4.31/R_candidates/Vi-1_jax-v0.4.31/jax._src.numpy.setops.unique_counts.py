def unique_counts(x: ArrayLike, /, *, size: int | None = None,
                  fill_value: ArrayLike | None = None) -> _UniqueCountsResult:
  """Return unique values from x, along with counts.

  JAX implementation of :func:`numpy.unique_counts`; this is equivalent to calling
  :func:`jax.numpy.unique` with `return_counts` and `equal_nan` set to True.

  Because the size of the output of ``unique_counts`` is data-dependent, the function
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
    A tuple ``(values, counts)``, with the following properties:

    - ``values``:
        an array of shape ``(n_unique,)`` containing the unique values from ``x``.
    - ``counts``:
        An array of shape ``(n_unique,)``. Contains the number of occurrences of each unique
        value in ``x``.

  See also:
    - :func:`jax.numpy.unique`: general function for computing unique values.
    - :func:`jax.numpy.unique_values`: compute only ``values``.
    - :func:`jax.numpy.unique_inverse`: compute only ``values`` and ``inverse``.
    - :func:`jax.numpy.unique_all`: compute ``values``, ``indices``, ``inverse_indices``,
      and ``counts``.

  Examples:
    Here we compute the unique values in a 1D array:

    >>> x = jnp.array([3, 4, 1, 3, 1])
    >>> result = jnp.unique_counts(x)

    The result is a :class:`~typing.NamedTuple` with two named attributes.
    The ``values`` attribute contains the unique values from the array:

    >>> result.values
    Array([1, 3, 4], dtype=int32)

    The ``counts`` attribute contains the counts of each unique value in the input:

    >>> result.counts
    Array([2, 2, 1], dtype=int32)

    For examples of the ``size`` and ``fill_value`` arguments, see :func:`jax.numpy.unique`.
  """
  check_arraylike("unique_counts", x)
  values, counts = unique(x, return_counts=True, equal_nan=False,
                          size=size, fill_value=fill_value)
  return _UniqueCountsResult(values=values, counts=counts)
