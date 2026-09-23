@_wraps(np.union1d,
  lax_description=_dedent("""
    Because the size of the output of ``union1d`` is data-dependent, the function is not
    typically compatible with JIT. The JAX version adds the optional ``size`` argument which
    must be specified statically for ``jnp.union1d`` to be used within some of JAX's
    transformations."""),
  extra_params=_dedent("""
    size : int, optional
        If specified, the first ``size`` elements of the result will be returned. If there are
        fewer elements than ``size`` indicates, the return value will be padded with ``fill_value``.
    fill_value : array_like, optional
        When ``size`` is specified and there are fewer than the indicated number of elements, the
        remaining elements will be filled with ``fill_value``, which defaults to the minimum
        value of the union."""))
def union1d(ar1, ar2, *, size=None, fill_value=None):
  _check_arraylike("union1d", ar1, ar2)
  if size is None:
    ar1 = core.concrete_or_error(None, ar1, "The error arose in union1d()")
    ar2 = core.concrete_or_error(None, ar2, "The error arose in union1d()")
  else:
    size = core.concrete_or_error(operator.index, size, "The error arose in union1d()")
  return unique(concatenate((ar1, ar2), axis=None), size=size, fill_value=fill_value)
