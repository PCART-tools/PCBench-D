@util._wraps(np.nonzero, lax_description=_NONZERO_DOC, extra_params=_NONZERO_EXTRA_PARAMS)
def nonzero(a: ArrayLike, *, size: Optional[int] = None,
            fill_value: Union[None, ArrayLike, Tuple[ArrayLike]] = None
    ) -> Tuple[Array, ...]:
  util.check_arraylike("nonzero", a)
  arr = atleast_1d(a)
  del a
  mask = arr if arr.dtype == bool else (arr != 0)
  if size is None:
    size = mask.sum()
  if not core.is_special_dim_size(size):
    size = core.concrete_or_error(operator.index, size,
      "The size argument of jnp.nonzero must be statically specified "
      "to use jnp.nonzero within JAX transformations.")
  if arr.size == 0 or size == 0:
    return tuple(zeros(size, int) for dim in arr.shape)
  flat_indices = reductions.cumsum(bincount(reductions.cumsum(mask), length=size))
  strides = (np.cumprod(arr.shape[::-1])[::-1] // arr.shape).astype(int_)
  out = tuple((flat_indices // stride) % size for stride, size in zip(strides, arr.shape))
  if size is not None and fill_value is not None:
    fill_value_tup = fill_value if isinstance(fill_value, tuple) else arr.ndim * (fill_value,)
    if _any(_shape(val) != () for val in fill_value_tup):
      raise ValueError(f"fill_value must be a scalar or a tuple of length {arr.ndim}; got {fill_value}")
    fill_mask = arange(size) >= mask.sum()
    out = tuple(where(fill_mask, fval, entry) for fval, entry in safe_zip(fill_value_tup, out))
  return out
