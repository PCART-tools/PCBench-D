@_wraps(np.block)
@jit
def block(arrays):
  out, _ = _block(arrays)
  return out
