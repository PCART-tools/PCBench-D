@_wraps(np.argwhere,
  lax_description=_dedent("""
    Because the size of the output of ``argwhere`` is data-dependent, the function is not
    typically compatible with JIT. The JAX version adds the optional ``size`` argument which
    must be specified statically for ``jnp.argwhere`` to be used within some of JAX's
    transformations."""),
  extra_params=_dedent("""
    size : int, optional
        If specified, the indices of the first ``size`` True elements will be returned. If there
        are fewer results than ``size`` indicates, the return value will be padded with ``fill_value``.
    fill_value : array_like, optional
        When ``size`` is specified and there are fewer than the indicated number of elements, the
        remaining elements will be filled with ``fill_value``, which defaults to zero."""))
def argwhere(a, *, size=None, fill_value=None):
  result = transpose(vstack(nonzero(a, size=size, fill_value=fill_value)))
  if ndim(a) == 0:
    return result[:0].reshape(result.shape[0], 0)
  return result.reshape(result.shape[0], ndim(a))
