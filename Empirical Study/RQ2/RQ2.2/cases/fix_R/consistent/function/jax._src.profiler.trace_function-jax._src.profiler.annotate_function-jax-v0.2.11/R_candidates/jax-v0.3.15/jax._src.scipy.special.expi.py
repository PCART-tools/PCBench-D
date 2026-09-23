@_wraps(osp_special.expi, module='scipy.special')
@api.custom_jvp
@jit
def expi(x):
  (x,) = _promote_args_inexact("expi", x)
  ret = jnp.piecewise(x, [x < 0], [lambda x: -exp1(-x), _expi_pos])
  return ret
