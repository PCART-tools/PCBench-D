@util._wraps(np.clip, skip_params=['out'])
@jit
def clip(a: ArrayLike, a_min: Optional[ArrayLike] = None,
         a_max: Optional[ArrayLike] = None, out: None = None) -> Array:
  util.check_arraylike("clip", a)
  if out is not None:
    raise NotImplementedError("The 'out' argument to jnp.clip is not supported.")
  if a_min is None and a_max is None:
    raise ValueError("At most one of a_min and a_max may be None")
  if a_min is not None:
    a = ufuncs.maximum(a_min, a)
  if a_max is not None:
    a = ufuncs.minimum(a_max, a)
  return asarray(a)
