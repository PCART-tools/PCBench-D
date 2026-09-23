@jit
def clip(
  arr: ArrayLike | None = None,
  /,
  min: ArrayLike | None = None,
  max: ArrayLike | None = None,
  *,
  a: ArrayLike | DeprecatedArg = DeprecatedArg(),
  a_min: ArrayLike | None | DeprecatedArg = DeprecatedArg(),
  a_max: ArrayLike | None | DeprecatedArg = DeprecatedArg()
) -> Array:
  """Clip array values to a specified range.

  JAX implementation of :func:`numpy.clip`.

  Args:
    arr: N-dimensional array to be clipped.
    min: optional minimum value of the clipped range; if ``None`` (default) then
      result will not be clipped to any minimum value. If specified, it should be
      broadcast-compatible with ``arr`` and ``max``.
    max: optional maximum value of the clipped range; if ``None`` (default) then
      result will not be clipped to any maximum value. If specified, it should be
      broadcast-compatible with ``arr`` and ``min``.
    a: deprecated alias of the ``arr`` argument.  Will result in a
      :class:`DeprecationWarning` if used.
    a_min: deprecated alias of the ``min`` argument. Will result in a
      :class:`DeprecationWarning` if used.
    a_max: deprecated alias of the ``max`` argument. Will result in a
      :class:`DeprecationWarning` if used.

  Returns:
    An array containing values from ``arr``, with values smaller than ``min`` set
    to ``min``, and values larger than ``max`` set to ``max``.

  See also:
    - :func:`jax.numpy.minimum`: Compute the element-wise minimum value of two arrays.
    - :func:`jax.numpy.maximum`: Compute the element-wise maximum value of two arrays.

  Examples:
    >>> arr = jnp.array([0, 1, 2, 3, 4, 5, 6, 7])
    >>> jnp.clip(arr, 2, 5)
    Array([2, 2, 2, 3, 4, 5, 5, 5], dtype=int32)
  """
  # TODO(micky774): deprecated 2024-4-2, remove after deprecation expires.
  arr = a if not isinstance(a, DeprecatedArg) else arr
  if arr is None:
    raise ValueError("No input was provided to the clip function.")
  min = a_min if not isinstance(a_min, DeprecatedArg) else min
  max = a_max if not isinstance(a_max, DeprecatedArg) else max
  if any(not isinstance(t, DeprecatedArg) for t in (a, a_min, a_max)):
    deprecations.warn(
      "jax-numpy-clip-args",
      ("Passing arguments 'a', 'a_min' or 'a_max' to jax.numpy.clip is "
       "deprecated. Please use 'arr', 'min' or 'max' respectively instead."),
      stacklevel=2,
    )

  util.check_arraylike("clip", arr)
  if any(jax.numpy.iscomplexobj(t) for t in (arr, min, max)):
    raise ValueError(
      "Clip received a complex value either through the input or the min/max "
      "keywords. Complex values have no ordering and cannot be clipped. "
      "Please convert to a real value or array by taking the real or "
      "imaginary components via jax.numpy.real/imag respectively.")
  if min is not None:
    arr = ufuncs.maximum(min, arr)
  if max is not None:
    arr = ufuncs.minimum(max, arr)
  return asarray(arr)
