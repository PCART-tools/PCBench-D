@implements(scipy.stats.sem, lax_description="""\
Currently the only supported nan_policies are 'propagate' and 'omit'
""")
@partial(jit, static_argnames=['axis', 'nan_policy', 'keepdims'])
def sem(a: ArrayLike, axis: int | None = 0, ddof: int = 1, nan_policy: str = "propagate", *, keepdims: bool = False) -> Array:
  b, = promote_args_inexact("sem", a)
  if axis is None:
    b = b.ravel()
    axis = 0
  if nan_policy == "propagate":
    return b.std(axis, ddof=ddof) / jnp.sqrt(b.shape[axis]).astype(b.dtype)
  elif nan_policy == "omit":
    count = (~jnp.isnan(b)).sum(axis)
    return jnp.nanstd(b, axis, ddof=ddof) / jnp.sqrt(count).astype(b.dtype)
  else:
    raise ValueError(f"{nan_policy} is not supported")
