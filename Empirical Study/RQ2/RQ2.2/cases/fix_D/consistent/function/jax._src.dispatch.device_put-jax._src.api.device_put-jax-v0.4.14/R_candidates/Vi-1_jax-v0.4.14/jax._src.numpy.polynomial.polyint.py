@_wraps(np.polyint)
@partial(jit, static_argnames=('m',))
def polyint(p: Array, m: int = 1, k: Optional[int] = None) -> Array:
  m = core.concrete_or_error(operator.index, m, "'m' argument of jnp.polyint")
  k = 0 if k is None else k
  check_arraylike("polyint", p, k)
  p, k_arr = promote_dtypes_inexact(p, k)
  if m < 0:
    raise ValueError("Order of integral must be positive (see polyder)")
  k_arr = atleast_1d(k_arr)
  if len(k_arr) == 1:
    k_arr = full((m,), k_arr[0])
  if k_arr.shape != (m,):
    raise ValueError("k must be a scalar or a rank-1 array of length 1 or m.")
  if m == 0:
    return p
  else:
    grid = (arange(len(p) + m, dtype=p.dtype)[np.newaxis]
            - arange(m, dtype=p.dtype)[:, np.newaxis])
    coeff = maximum(1, grid).prod(0)[::-1]
    return true_divide(concatenate((p, k_arr)), coeff)
