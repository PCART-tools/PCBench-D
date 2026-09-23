@_wraps(np.nonzero, lax_description=_NONZERO_DOC, extra_params=_NONZERO_EXTRA_PARAMS)
def nonzero(a, *, size=None, fill_value=None):
  _check_arraylike("nonzero", a)
  a = atleast_1d(a)
  mask = a if a.dtype == bool else (a != 0)
  if size is None:
    size = mask.sum()
  size = core.concrete_or_error(operator.index, size,
    "The size argument of jnp.nonzero must be statically specified "
    "to use jnp.nonzero within JAX transformations.")
  if a.size == 0 or size == 0:
    return tuple(zeros(size, int) for dim in a.shape)
  flat_indices = cumsum(bincount(cumsum(mask), length=size))
  strides = (np.cumprod(a.shape[::-1])[::-1] // a.shape).astype(int_)
  out = tuple((flat_indices // stride) % size for stride, size in zip(strides, a.shape))
  if size is not None and fill_value is not None:
    if not isinstance(fill_value, tuple):
      fill_value = a.ndim * (fill_value,)
    if _shape(fill_value) != (a.ndim,):
      raise ValueError(f"fill_value must be a scalar or a tuple of length {a.ndim}; got {fill_value}")
    fill_mask = arange(size) >= mask.sum()
    out = tuple(where(fill_mask, fval, entry) for fval, entry in safe_zip(fill_value, out))
  return out
