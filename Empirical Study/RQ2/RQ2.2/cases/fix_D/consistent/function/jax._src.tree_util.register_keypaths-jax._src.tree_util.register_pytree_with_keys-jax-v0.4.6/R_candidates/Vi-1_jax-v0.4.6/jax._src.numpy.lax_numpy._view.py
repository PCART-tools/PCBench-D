def _view(arr: Array, dtype: DTypeLike = None, type: None = None) -> Array:
  """Return a bitwise copy of the array, viewed as a new dtype.

  This is fuller-featured wrapper around :func:`jax.lax.bitcast_convert_type`.

  If the source and target dtype have the same bitwidth, the result has the same
  shape as the input array. If the bitwidth of the target dtype is different
  from the source, the size of the last axis of the result is adjusted
  accordingly.

  >>> jnp.zeros([1,2,3], dtype=jnp.int16).view(jnp.int8).shape
  (1, 2, 6)
  >>> jnp.zeros([1,2,4], dtype=jnp.int8).view(jnp.int16).shape
  (1, 2, 2)

  Conversions involving booleans are not well-defined in all situations. With
  regards to the shape of result as explained above, booleans are treated as
  having a bitwidth of 8. However, when converting to a boolean array, the input
  should only contain 0 or 1 bytes. Otherwise, results may be unpredictable or
  may change depending on how the result is used.

  This conversion is guaranteed and safe:
  >>> jnp.array([1, 0, 1], dtype=jnp.int8).view(jnp.bool_)
  Array([ True, False,  True], dtype=bool)

  However, there are no guarantees about the results of any expression involving
  a view such as this: `jnp.array([1, 2, 3], dtype=jnp.int8).view(jnp.bool_)`.
  In particular, the results may change between JAX releases and depending on
  the platform. To safely convert such an array to a boolean array, compare it
  with `0`:

  >>> jnp.array([1, 2, 0], dtype=jnp.int8) != 0
  Array([ True,  True, False], dtype=bool)
  """
  if type is not None:
    raise NotImplementedError("`type` argument of array.view() is not supported.")

  util._check_arraylike("view", arr)
  arr = asarray(arr)

  dtypes.check_user_dtype_supported(dtype, "view")
  dtype = dtypes.canonicalize_dtype(dtype)

  if arr.ndim == 0:
    if arr.dtype.itemsize != dtype.itemsize:
      raise ValueError("view() of a 0d array is only supported if the itemsize is unchanged.")
    return _view(lax.expand_dims(arr, (0,)), dtype).squeeze()

  if (arr.shape[-1] * arr.dtype.itemsize) % dtype.itemsize != 0:
    raise ValueError("When changing to a larger dtype, its size must be a divisor "
                     "of the total size in bytes of the last axis of the array.")

  if arr.dtype == dtype:
    return arr

  # lax.bitcast_convert_type does not support bool or complex; in these cases we
  # cast to a compatible type and recursively call _view for simplicity.
  if arr.dtype == bool:
    return _view(arr.astype('uint8'), dtype)

  if issubdtype(arr.dtype, complexfloating):
    new_shape = (*arr.shape[:-1], arr.shape[-1] * 2)
    new_dtype = finfo(arr.dtype).dtype
    arr = (zeros(new_shape, new_dtype)
             .at[..., 0::2].set(arr.real)
             .at[..., 1::2].set(arr.imag))
    return _view(arr, dtype)

  if dtype == bool:
    return _view(arr, uint8).astype(bool)

  if issubdtype(dtype, complexfloating):
    out = _view(arr, finfo(dtype).dtype).astype(dtype)
    return out[..., 0::2] + 1j * out[..., 1::2]

  # lax.bitcast_convert_type adds or subtracts dimensions depending on the
  # relative bitwidths of the dtypes; we account for that with reshapes.
  if arr.dtype.itemsize < dtype.itemsize:
    factor = dtype.itemsize // arr.dtype.itemsize
    arr = arr.reshape(*arr.shape[:-1], arr.shape[-1] // factor, factor)
    return lax.bitcast_convert_type(arr, dtype)

  if arr.dtype.itemsize > dtype.itemsize:
    out = lax.bitcast_convert_type(arr, dtype)
    return out.reshape(*out.shape[:-2], out.shape[-2] * out.shape[-1])

  return lax.bitcast_convert_type(arr, dtype)
