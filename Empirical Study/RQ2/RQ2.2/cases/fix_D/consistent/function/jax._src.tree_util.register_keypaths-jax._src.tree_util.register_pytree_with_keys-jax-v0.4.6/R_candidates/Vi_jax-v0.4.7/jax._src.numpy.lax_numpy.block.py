@util._wraps(np.block)
@jit
def block(arrays: Union[ArrayLike, List[ArrayLike]]) -> Array:
  out, _ = _block(arrays)
  return out
