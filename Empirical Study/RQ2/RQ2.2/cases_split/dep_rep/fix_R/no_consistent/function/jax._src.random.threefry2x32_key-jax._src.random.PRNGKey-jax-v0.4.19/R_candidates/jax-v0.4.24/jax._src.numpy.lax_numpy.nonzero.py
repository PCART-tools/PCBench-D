@util.implements(np.nonzero, lax_description=_NONZERO_DOC, extra_params=_NONZERO_EXTRA_PARAMS)
def nonzero(a: ArrayLike, *, size: int | None = None,
            fill_value: None | ArrayLike | tuple[ArrayLike, ...] = None
    ) -> tuple[Array, ...]:
  util.check_arraylike("nonzero", a)
  arr = asarray(a)
  del a
  if ndim(arr) == 0:
    # Added 2023 Dec 6
    warnings.warn("Calling nonzero on 0d arrays is deprecated. Use `atleast_1d(arr).nonzero()",
                  DeprecationWarning, stacklevel=2)
  arr = atleast_1d(arr)
  mask = arr if arr.dtype == bool else (arr != 0)
  calculated_size = mask.sum() if size is None else size
  calculated_size = core.concrete_dim_or_error(calculated_size,
    "The size argument of jnp.nonzero must be statically specified "
    "to use jnp.nonzero within JAX transformations.")
  if arr.size == 0 or calculated_size == 0:
    return tuple(zeros(calculated_size, int) for dim in arr.shape)
  flat_indices = reductions.cumsum(
      bincount(reductions.cumsum(mask),
               length=calculated_size))  # type: ignore[arg-type]
  strides: np.ndarray = (np.cumprod(arr.shape[::-1])[::-1] // arr.shape).astype(int_)
  out = tuple((flat_indices // stride) % size for stride, size in zip(strides, arr.shape))
  if fill_value is not None:
    fill_value_tup = fill_value if isinstance(fill_value, tuple) else arr.ndim * (fill_value,)
    if any(_shape(val) != () for val in fill_value_tup):
      raise ValueError(f"fill_value must be a scalar or a tuple of length {arr.ndim}; got {fill_value}")
    fill_mask = arange(calculated_size) >= mask.sum()
    out = tuple(where(fill_mask, fval, entry) for fval, entry in safe_zip(fill_value_tup, out))
  return out
