def extract(condition: ArrayLike, arr: ArrayLike,
            *, size: int | None = None, fill_value: ArrayLike = 0) -> Array:
  """Return the elements of an array that satisfy a condition.

  JAX implementation of :func:`numpy.extract`.

  Args:
    condition: array of conditions. Will be converted to boolean and flattened to 1D.
    arr: array of values to extract. Will be flattened to 1D.
    size: optional static size for output. Must be specified in order for ``extract``
      to be compatible with JAX transformations like :func:`~jax.jit` or :func:`~jax.vmap`.
    fill_value: if ``size`` is specified, fill padded entries with this value (default: 0).

  Returns:
    1D array of extracted entries . If ``size`` is specified, the result will have shape
    ``(size,)`` and be right-padded with ``fill_value``. If ``size`` is not specified,
    the output shape will depend on the number of True entries in ``condition``.

  Notes:
    This function does not require strict shape agreement between ``condition`` and ``arr``.
    If ``condition.size > arr.size``, then ``condition`` will be truncated, and if
    ``arr.size > condition.size``, then ``arr`` will be truncated.

  See also:
    :func:`jax.numpy.compress`: multi-dimensional version of ``extract``.

  Examples:
     Extract values from a 1D array:

     >>> x = jnp.array([1, 2, 3, 4, 5, 6])
     >>> mask = (x % 2 == 0)
     >>> jnp.extract(mask, x)
     Array([2, 4, 6], dtype=int32)

     In the simplest case, this is equivalent to boolean indexing:

     >>> x[mask]
     Array([2, 4, 6], dtype=int32)

     For use with JAX transformations, you can pass the ``size`` argument to
     specify a static shape for the output, along with an optional ``fill_value``
     that defaults to zero:

     >>> jnp.extract(mask, x, size=len(x), fill_value=0)
     Array([2, 4, 6, 0, 0, 0], dtype=int32)

     Notice that unlike with boolean indexing, ``extract`` does not require strict
     agreement between the sizes of the array and condition, and will effectively
     truncate both to the minimum size:

     >>> short_mask = jnp.array([False, True])
     >>> jnp.extract(short_mask, x)
     Array([2], dtype=int32)
     >>> long_mask = jnp.array([True, False, True, False, False, False, False, False])
     >>> jnp.extract(long_mask, x)
     Array([1, 3], dtype=int32)
  """
  util.check_arraylike("extreact", condition, arr, fill_value)
  return compress(ravel(condition), ravel(arr), size=size, fill_value=fill_value)
