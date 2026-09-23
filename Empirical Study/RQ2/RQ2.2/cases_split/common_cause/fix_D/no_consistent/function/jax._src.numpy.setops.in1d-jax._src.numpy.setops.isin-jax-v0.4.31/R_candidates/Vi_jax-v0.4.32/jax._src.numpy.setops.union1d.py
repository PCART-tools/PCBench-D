def union1d(ar1: ArrayLike, ar2: ArrayLike,
            *, size: int | None = None, fill_value: ArrayLike | None = None) -> Array:
  """Compute the set union of two 1D arrays.

  JAX implementation of :func:`numpy.union1d`.

  Because the size of the output of ``union1d`` is data-dependent, the function
  is not typically compatible with :func:`~jax.jit` and other JAX transformations.
  The JAX version adds the optional ``size`` argument which must be specified
  statically for ``jnp.union1d`` to be used in such contexts.

  Args:
    ar1: first array of elements to be unioned.
    ar2: second array of elements to be unioned
    size: if specified, return only the first ``size`` sorted elements. If there are fewer
      elements than ``size`` indicates, the return value will be padded with ``fill_value``.
    fill_value: when ``size`` is specified and there are fewer than the indicated number of
      elements, fill the remaining entries ``fill_value``. Defaults to the minimum value.

  Returns:
    an array containing the union of elements in the input array.

  See also:
    - :func:`jax.numpy.intersect1d`: the set intersection of two 1D arrays.
    - :func:`jax.numpy.setxor1d`: the set XOR of two 1D arrays.
    - :func:`jax.numpy.setdiff1d`: the set difference of two 1D arrays.

  Examples:
    Computing the union of two arrays:

    >>> ar1 = jnp.array([1, 2, 3, 4])
    >>> ar2 = jnp.array([3, 4, 5, 6])
    >>> jnp.union1d(ar1, ar2)
    Array([1, 2, 3, 4, 5, 6], dtype=int32)

    Because the output shape is dynamic, this will fail under :func:`~jax.jit` and other
    transformations:

    >>> jax.jit(jnp.union1d)(ar1, ar2)  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
       ...
    ConcretizationTypeError: Abstract tracer value encountered where concrete value is expected: traced array with shape int32[4].
    The error occurred while tracing the function union1d at /Users/vanderplas/github/google/jax/jax/_src/numpy/setops.py:101 for jit. This concrete value was not available in Python because it depends on the value of the argument ar1.

    In order to ensure statically-known output shapes, you can pass a static ``size``
    argument:

    >>> jit_union1d = jax.jit(jnp.union1d, static_argnames=['size'])
    >>> jit_union1d(ar1, ar2, size=6)
    Array([1, 2, 3, 4, 5, 6], dtype=int32)

    If ``size`` is too small, the union is truncated:

    >>> jit_union1d(ar1, ar2, size=4)
    Array([1, 2, 3, 4], dtype=int32)

    If ``size`` is too large, then the output is padded with ``fill_value``:

    >>> jit_union1d(ar1, ar2, size=8, fill_value=0)
    Array([1, 2, 3, 4, 5, 6, 0, 0], dtype=int32)
  """
  check_arraylike("union1d", ar1, ar2)
  if size is None:
    ar1 = core.concrete_or_error(None, ar1, "The error arose in union1d()")
    ar2 = core.concrete_or_error(None, ar2, "The error arose in union1d()")
  else:
    size = core.concrete_or_error(operator.index, size, "The error arose in union1d()")
  out = unique(concatenate((ar1, ar2), axis=None), size=size,
               fill_value=fill_value)
  return cast(Array, out)
