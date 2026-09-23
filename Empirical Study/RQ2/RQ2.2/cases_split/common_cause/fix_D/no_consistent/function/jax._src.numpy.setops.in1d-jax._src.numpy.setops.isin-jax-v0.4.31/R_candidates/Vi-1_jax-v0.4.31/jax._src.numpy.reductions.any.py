def any(a: ArrayLike, axis: Axis = None, out: None = None,
        keepdims: bool = False, *, where: ArrayLike | None = None) -> Array:
  r"""Test whether any of the array elements along a given axis evaluate to True.

  JAX implementation of :func:`numpy.any`.

  Args:
    a: Input array.
    axis: int or array, default=None. Axis along which to be tested. If None,
      tests along all the axes.
    keepdims: bool, default=False. If true, reduced axes are left in the result
      with size 1.
    where: int or array of boolean dtype, default=None. The elements to be used
      in the test. Array should be broadcast compatible to the input.
    out: Unused by JAX.

  Returns:
    An array of boolean values.

  Examples:
    By default, ``jnp.any`` tests along all the axes.

    >>> x = jnp.array([[True, True, True, False],
    ...                [True, False, True, False],
    ...                [True, True, False, False]])
    >>> jnp.any(x)
    Array(True, dtype=bool)

    If ``axis=0``, tests along axis 0.

    >>> jnp.any(x, axis=0)
    Array([ True,  True,  True, False], dtype=bool)

    If ``keepdims=True``, ``ndim`` of the output will be same of that of the input.

    >>> jnp.any(x, axis=0, keepdims=True)
    Array([[ True,  True,  True, False]], dtype=bool)

    To include specific elements in testing for True values, you can use a``where``.

    >>> where=jnp.array([[1, 0, 1, 0],
    ...                  [0, 1, 0, 1],
    ...                  [1, 0, 1, 0]], dtype=bool)
    >>> jnp.any(x, axis=0, keepdims=True, where=where)
    Array([[ True, False,  True, False]], dtype=bool)
  """
  return _reduce_any(a, axis=_ensure_optional_axes(axis), out=out,
                     keepdims=keepdims, where=where)
