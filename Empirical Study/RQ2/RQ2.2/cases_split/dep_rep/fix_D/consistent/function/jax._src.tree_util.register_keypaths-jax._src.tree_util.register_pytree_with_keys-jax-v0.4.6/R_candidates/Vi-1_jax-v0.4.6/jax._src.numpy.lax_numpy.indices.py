@util._wraps(np.indices)
def indices(dimensions: Sequence[int], dtype: DTypeLike = int32,
            sparse: bool = False) -> Union[Array, Tuple[Array, ...]]:
  dimensions = tuple(
      core.concrete_or_error(operator.index, d, "dimensions argument of jnp.indices")
      for d in dimensions)
  N = len(dimensions)
  output = []
  s = dimensions
  for i, dim in enumerate(dimensions):
    idx = lax.iota(dtype, dim)
    if sparse:
      s = (1,)*i + (dim,) + (1,)*(N - i - 1)
    output.append(lax.broadcast_in_dim(idx, s, (i,)))
  if sparse:
    return tuple(output)
  return stack(output, 0) if output else array([], dtype=dtype)
