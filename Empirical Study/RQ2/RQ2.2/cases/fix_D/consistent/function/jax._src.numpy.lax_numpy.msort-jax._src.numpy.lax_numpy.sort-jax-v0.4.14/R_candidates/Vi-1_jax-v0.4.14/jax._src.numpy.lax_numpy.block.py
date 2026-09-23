@util._wraps(np.block)
@jit
def block(arrays: Union[ArrayLike, list[ArrayLike]]) -> Array:
  out, _ = _block(arrays)
  return out
