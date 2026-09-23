@implements(scipy.linalg.block_diag)
@jit
def block_diag(*arrs: ArrayLike) -> Array:
  if len(arrs) == 0:
    arrs = cast(tuple[ArrayLike], (jnp.zeros((1, 0)),))
  arrs = cast(tuple[ArrayLike], promote_dtypes(*arrs))
  bad_shapes = [i for i, a in enumerate(arrs) if jnp.ndim(a) > 2]
  if bad_shapes:
    raise ValueError("Arguments to jax.scipy.linalg.block_diag must have at "
                     "most 2 dimensions, got {} at argument {}."
                     .format(arrs[bad_shapes[0]], bad_shapes[0]))
  converted_arrs = [jnp.atleast_2d(a) for a in arrs]
  acc = converted_arrs[0]
  dtype = lax.dtype(acc)
  for a in converted_arrs[1:]:
    _, c = a.shape
    a = lax.pad(a, dtype.type(0), ((0, 0, 0), (acc.shape[-1], 0, 0)))
    acc = lax.pad(acc, dtype.type(0), ((0, 0, 0), (0, c, 0)))
    acc = lax.concatenate([acc, a], dimension=0)
  return acc
