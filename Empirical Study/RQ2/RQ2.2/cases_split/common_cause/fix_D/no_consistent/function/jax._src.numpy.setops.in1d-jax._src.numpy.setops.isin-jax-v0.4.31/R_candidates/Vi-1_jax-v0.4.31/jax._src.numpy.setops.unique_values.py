def unique_values(x: ArrayLike, /, *, size: int | None = None,
                  fill_value: ArrayLike | None = None) -> Array:
  """Return unique values from x, along with indices, inverse indices, and counts.

  JAX implementation of :func:`numpy.unique_values`; this is equivalent to calling
  :func:`jax.numpy.unique` with `equal_nan` set to True.

  Because the size of the output of ``unique_values`` is data-dependent, the function
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
    An array ``values`` of shape ``(n_unique,)`` containing the unique values from ``x``.

  See also:
    - :func:`jax.numpy.unique`: general function for computing unique values.
    - :func:`jax.numpy.unique_values`: compute only ``values``.
    - :func:`jax.numpy.unique_counts`: compute only ``values`` and ``counts``.
    - :func:`jax.numpy.unique_inverse`: compute only ``values`` and ``inverse``.

  Examples:
    Here we compute the unique values in a 1D array:

    >>> x = jnp.array([3, 4, 1, 3, 1])
    >>> jnp.unique_values(x)
    Array([1, 3, 4], dtype=int32)

    For examples of the ``size`` and ``fill_value`` arguments, see :func:`jax.numpy.unique`.
  """
  check_arraylike("unique_values", x)
  return cast(Array, unique(x, equal_nan=False, size=size, fill_value=fill_value))
