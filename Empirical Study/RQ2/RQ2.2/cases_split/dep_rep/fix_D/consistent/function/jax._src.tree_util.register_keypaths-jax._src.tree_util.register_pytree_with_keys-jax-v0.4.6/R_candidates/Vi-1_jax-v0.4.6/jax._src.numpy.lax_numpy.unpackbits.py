@util._wraps(np.unpackbits)
@partial(jit, static_argnames=('axis', 'count', 'bitorder'))
def unpackbits(a, axis: Optional[int] = None, count=None, bitorder='big'):
  util._check_arraylike("unpackbits", a)
  if _dtype(a) != uint8:
    raise TypeError("Expected an input array of unsigned byte data type")
  if bitorder not in ['little', 'big']:
    raise ValueError("'order' must be either 'little' or 'big'")
  bits = asarray(1) << arange(8, dtype='uint8')
  if bitorder == 'big':
    bits = bits[::-1]
  if axis is None:
    a = ravel(a)
    axis = 0
  a = swapaxes(a, axis, -1)
  unpacked = ((a[..., None] & expand_dims(bits, tuple(range(a.ndim)))) > 0).astype('uint8')
  unpacked = unpacked.reshape(unpacked.shape[:-2] + (-1,))[..., :count]
  return swapaxes(unpacked, axis, -1)
