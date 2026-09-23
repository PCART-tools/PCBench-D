@util._wraps(np.unpackbits)
@partial(jit, static_argnames=('axis', 'count', 'bitorder'))
def unpackbits(
    a: ArrayLike,
    axis: int | None = None,
    count: int | None = None,
    bitorder: str = "big",
) -> Array:
  util.check_arraylike("unpackbits", a)
  arr = asarray(a)
  if _dtype(a) != uint8:
    raise TypeError("Expected an input array of unsigned byte data type")
  if bitorder not in ['little', 'big']:
    raise ValueError("'order' must be either 'little' or 'big'")
  bits = asarray(1) << arange(8, dtype='uint8')
  if bitorder == 'big':
    bits = bits[::-1]
  if axis is None:
    arr = ravel(arr)
    axis = 0
  arr = swapaxes(arr, axis, -1)
  unpacked = ((arr[..., None] & expand_dims(bits, tuple(range(arr.ndim)))) > 0).astype('uint8')
  unpacked = unpacked.reshape(unpacked.shape[:-2] + (-1,))
  if count is not None:
    if count > unpacked.shape[-1]:
      unpacked = pad(unpacked, [(0, 0)] * (unpacked.ndim - 1) + [(0, count - unpacked.shape[-1])])
    else:
      unpacked = unpacked[..., :count]
  return swapaxes(unpacked, axis, -1)
