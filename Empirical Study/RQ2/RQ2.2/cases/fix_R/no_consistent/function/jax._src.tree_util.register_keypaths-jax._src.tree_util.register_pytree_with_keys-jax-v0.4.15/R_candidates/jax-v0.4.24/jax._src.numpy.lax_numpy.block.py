@util.implements(np.block)
@jit
def block(arrays: ArrayLike | list[ArrayLike]) -> Array:
  out, _ = _block(arrays)
  return out
