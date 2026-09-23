@util._wraps(np.packbits)
@partial(jit, static_argnames=('axis', 'bitorder'))
def packbits(
    a: ArrayLike, axis: int | None = None, bitorder: str = "big"
) -> Array:
  util.check_arraylike("packbits", a)
  arr = asarray(a)
  if not (issubdtype(arr.dtype, integer) or issubdtype(arr.dtype, bool_)):
    raise TypeError('Expected an input array of integer or boolean data type')
  if bitorder not in ['little', 'big']:
    raise ValueError("'order' must be either 'little' or 'big'")
  arr = lax.gt(arr, _lax_const(a, 0)).astype('uint8')
  bits = arange(8, dtype='uint8')
  if bitorder == 'big':
    bits = bits[::-1]
  if axis is None:
    arr = ravel(arr)
    axis = 0
  arr = swapaxes(arr, axis, -1)

  remainder = arr.shape[-1] % 8
  if remainder:
    arr = lax.pad(arr, np.uint8(0),
                  (arr.ndim - 1) * [(0, 0, 0)] + [(0, 8 - remainder, 0)])

  arr = arr.reshape(arr.shape[:-1] + (arr.shape[-1] // 8, 8))
  bits = expand_dims(bits, tuple(range(arr.ndim - 1)))
  packed = (arr << bits).sum(-1).astype('uint8')
  return swapaxes(packed, axis, -1)
