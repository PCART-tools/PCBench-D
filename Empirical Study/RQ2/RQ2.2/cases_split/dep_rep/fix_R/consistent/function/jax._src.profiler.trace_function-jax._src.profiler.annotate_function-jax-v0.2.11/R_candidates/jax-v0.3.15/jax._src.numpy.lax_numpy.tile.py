@_wraps(np.tile)
def tile(A, reps):
  _stackable(A) or _check_arraylike("tile", A)
  try:
    iter(reps)
  except TypeError:
    reps = (reps,)
  reps = tuple(operator.index(rep) if core.is_constant_dim(rep) else rep
               for rep in reps)
  A_shape = (1,) * (len(reps) - ndim(A)) + shape(A)
  reps = (1,) * (len(A_shape) - len(reps)) + reps
  result = broadcast_to(reshape(A, [j for i in A_shape for j in [1, i]]),
                        [k for pair in zip(reps, A_shape) for k in pair])
  return reshape(result, tuple(np.multiply(A_shape, reps)))
