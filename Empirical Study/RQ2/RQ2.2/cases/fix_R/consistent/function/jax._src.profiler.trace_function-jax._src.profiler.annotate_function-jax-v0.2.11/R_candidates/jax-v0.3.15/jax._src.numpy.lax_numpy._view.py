def _view(arr, dtype=None, type=None):
  lax_internal._check_user_dtype_supported(dtype, "view")
  if type is not None:
    raise NotImplementedError("`type` argument of array.view()")
  if dtype is None:
    return arr
  arr_dtype = _dtype(arr)
  if arr_dtype == dtype:
    return arr
  # bool is implemented as lax:PRED, which is not compatible with lax.bitcast_convert_type.
  # We work around this by casting bool to uint8.
  if arr_dtype == bool_:
    arr = arr.astype(uint8)
  nbits_in = 8 * arr_dtype.itemsize
  nbits_out = 8 * np.dtype(dtype).itemsize
  if nbits_in == nbits_out:
    if dtype == bool_:
      return lax.bitcast_convert_type(arr, uint8).astype(dtype)
    return lax.bitcast_convert_type(arr, dtype)
  if nbits_out > nbits_in and (shape(arr)[-1] * nbits_in) % nbits_out != 0:
    raise ValueError("When changing to a larger dtype, its size must be a divisor "
                     "of the total size in bytes of the last axis of the array.")
  byte_dtypes = {8: uint8, 16: uint16, 32: uint32, 64: uint64}
  if nbits_in not in byte_dtypes:
    raise NotImplementedError(f"arr.view() for arr.dtype={arr_dtype}")
  if nbits_out not in byte_dtypes:
    raise NotImplementedError(f"arr.view(dtype) for dtype={dtype}")
  dt_in = byte_dtypes[nbits_in]
  dt_out = byte_dtypes[nbits_out]
  arr_bytes = lax.bitcast_convert_type(arr, dt_in)
  if nbits_in < nbits_out:
    arr_bytes = arr_bytes.reshape(arr.shape[:-1] + (-1, nbits_out // nbits_in)).astype(dt_out)
    shifts = expand_dims(arange(0, nbits_out, nbits_in, dtype=dt_out), tuple(range(arr_bytes.ndim - 1)))
    arr_bytes = (arr_bytes << shifts).sum(-1).astype(dt_out)
  else:
    shifts = lax.expand_dims(arange(0, nbits_in, nbits_out, dtype=dt_in), tuple(range(arr_bytes.ndim)))
    arr_bytes = ((arr_bytes[..., newaxis] >> shifts) & iinfo(dt_out).max).astype(dt_out)
    arr_bytes = arr_bytes.reshape(arr_bytes.shape[:-2] + (-1,))
  if dtype == bool_:
    return lax.bitcast_convert_type(arr_bytes, uint8).astype(dtype)
  return lax.bitcast_convert_type(arr_bytes, dtype)
