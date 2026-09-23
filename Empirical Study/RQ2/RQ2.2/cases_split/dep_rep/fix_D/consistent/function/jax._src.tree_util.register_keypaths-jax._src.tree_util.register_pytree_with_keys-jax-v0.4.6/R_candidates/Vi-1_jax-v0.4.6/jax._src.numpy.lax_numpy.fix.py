@util._wraps(np.fix, skip_params=['out'])
@jit
def fix(x: ArrayLike, out: None = None) -> Array:
  util._check_arraylike("fix", x)
  if out is not None:
    raise NotImplementedError("The 'out' argument to jnp.fix is not supported.")
  zero = _lax_const(x, 0)
  return where(lax.ge(x, zero), ufuncs.floor(x), ufuncs.ceil(x))
