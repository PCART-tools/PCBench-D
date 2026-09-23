@implements(np.unique, skip_params=['axis'],
  lax_description=_dedent("""
    Because the size of the output of ``unique`` is data-dependent, the function is not
    typically compatible with JIT. The JAX version adds the optional ``size`` argument which
    must be specified statically for ``jnp.unique`` to be used within some of JAX's
    transformations."""),
  extra_params=_dedent("""
    size : int, optional
        If specified, the first ``size`` unique elements will be returned. If there are fewer unique
        elements than ``size`` indicates, the return value will be padded with ``fill_value``.
    fill_value : array_like, optional
        When ``size`` is specified and there are fewer than the indicated number of elements, the
        remaining elements will be filled with ``fill_value``. The default is the minimum value
        along the specified axis of the input."""))
def unique(ar: ArrayLike, return_index: bool = False, return_inverse: bool = False,
           return_counts: bool = False, axis: int | None = None,
           *, equal_nan: bool = True, size: int | None = None, fill_value: ArrayLike | None = None):
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
