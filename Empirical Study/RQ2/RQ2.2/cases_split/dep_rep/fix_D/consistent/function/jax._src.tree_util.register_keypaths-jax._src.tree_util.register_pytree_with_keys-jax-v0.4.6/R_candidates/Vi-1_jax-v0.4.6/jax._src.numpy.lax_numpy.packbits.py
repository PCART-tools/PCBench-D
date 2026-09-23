@util._wraps(np.packbits)
@partial(jit, static_argnames=('axis', 'bitorder'))
def packbits(a, axis: Optional[int] = None, bitorder='big'):
  util._check_arraylike("packbits", a)
  if not (issubdtype(_dtype(a), integer) or issubdtype(_dtype(a), bool_)):
    raise TypeError('Expected an input array of integer or boolean data type')
  if bitorder not in ['little', 'big']:
    raise ValueError("'order' must be either 'little' or 'big'")
  a = lax.gt(a, _lax_const(a, 0)).astype('uint8')
  bits = arange(8, dtype='uint8')
  if bitorder == 'big':
    bits = bits[::-1]
  if axis is None:
    a = ravel(a)
    axis = 0
  a = swapaxes(a, axis, -1)

  remainder = a.shape[-1] % 8
  if remainder:
    a = lax.pad(a, np.uint8(0),
                (a.ndim - 1) * [(0, 0, 0)] + [(0, 8 - remainder, 0)])

  a = a.reshape(a.shape[:-1] + (a.shape[-1] // 8, 8))
  bits = expand_dims(bits, tuple(range(a.ndim - 1)))
  packed = (a << bits).sum(-1).astype('uint8')
  return swapaxes(packed, axis, -1)
