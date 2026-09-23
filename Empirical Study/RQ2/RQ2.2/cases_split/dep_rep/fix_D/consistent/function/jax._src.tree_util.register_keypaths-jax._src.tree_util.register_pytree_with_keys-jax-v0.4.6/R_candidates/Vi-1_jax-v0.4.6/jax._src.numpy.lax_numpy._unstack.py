@jit
def _unstack(x: Array) -> List[Array]:
  return [lax.index_in_dim(x, i, keepdims=False) for i in range(x.shape[0])]
