@_wraps(np.where,
  lax_description=_dedent("""
    At present, JAX does not support JIT-compilation of the single-argument form
    of :py:func:`jax.numpy.where` because its output shape is data-dependent. The
    three-argument form does not have a data-dependent shape and can be JIT-compiled
    successfully. Alternatively, you can use the optional ``size`` keyword to
    statically specify the expected size of the output."""),
  extra_params=_dedent("""
    size : int, optional
        Only referenced when ``x`` and ``y`` are ``None``. If specified, the indices of the first
        ``size`` elements of the result will be returned. If there are fewer elements than ``size``
        indicates, the return value will be padded with ``fill_value``.
    fill_value : array_like, optional
        When ``size`` is specified and there are fewer than the indicated number of elements, the
        remaining elements will be filled with ``fill_value``, which defaults to zero."""))
def where(condition, x=None, y=None, *, size=None, fill_value=None):
  if x is None and y is None:
    _check_arraylike("where", condition)
    return nonzero(condition, size=size, fill_value=fill_value)
  else:
    _check_arraylike("where", condition, x, y)
    if size is not None or fill_value is not None:
      raise ValueError("size and fill_value arguments cannot be used in three-term where function.")
    return _where(condition, x, y)
