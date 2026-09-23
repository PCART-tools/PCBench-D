@_wraps(np.unique, skip_params=['axis'],
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
def unique(ar, return_index=False, return_inverse=False,
           return_counts=False, axis: Optional[int] = None, *, size=None, fill_value=None):
  _check_arraylike("unique", ar)
  if size is None:
    ar = core.concrete_or_error(None, ar,
        "The error arose for the first argument of jnp.unique(). " + UNIQUE_SIZE_HINT)
  else:
    size = core.concrete_or_error(operator.index, size,
         "The error arose for the size argument of jnp.unique(). " + UNIQUE_SIZE_HINT)
  ar = asarray(ar)
  if axis is None:
    axis = 0
    ar = ar.flatten()
  axis = core.concrete_or_error(operator.index, axis, "axis argument of jnp.unique()")
  return _unique(ar, axis, return_index, return_inverse, return_counts, size=size, fill_value=fill_value)
