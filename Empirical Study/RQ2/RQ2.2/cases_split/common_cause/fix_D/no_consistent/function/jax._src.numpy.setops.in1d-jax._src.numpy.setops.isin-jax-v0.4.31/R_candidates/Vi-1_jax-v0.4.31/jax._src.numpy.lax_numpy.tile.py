@util.implements(np.tile)
def tile(A: ArrayLike, reps: DimSize | Sequence[DimSize]) -> Array:
  util.check_arraylike("tile", A)
  try:
    iter(reps)  # type: ignore[arg-type]
  except TypeError:
    reps_tup: tuple[DimSize, ...] = (reps,)
  else:
    reps_tup = tuple(reps)  # type: ignore[arg-type]
  reps_tup = tuple(operator.index(rep) if core.is_constant_dim(rep) else rep
                   for rep in reps_tup)
  A_shape = (1,) * (len(reps_tup) - ndim(A)) + shape(A)
  reps_tup = (1,) * (len(A_shape) - len(reps_tup)) + reps_tup
  result = broadcast_to(reshape(A, [j for i in A_shape for j in [1, i]]),
                        [k for pair in zip(reps_tup, A_shape) for k in pair])
  return reshape(result, tuple(np.multiply(A_shape, reps_tup)))
