def clz(x):
  assert np.issubdtype(x.dtype, np.integer)
  nbits = np.iinfo(x.dtype).bits
  mask = (2 ** np.arange(nbits, dtype=x.dtype))[::-1]
  bits = (x[..., None] & mask).astype(np.bool_)
  out = np.argmax(bits, axis=-1).astype(x.dtype)
  out[x == 0] = nbits
  return out
