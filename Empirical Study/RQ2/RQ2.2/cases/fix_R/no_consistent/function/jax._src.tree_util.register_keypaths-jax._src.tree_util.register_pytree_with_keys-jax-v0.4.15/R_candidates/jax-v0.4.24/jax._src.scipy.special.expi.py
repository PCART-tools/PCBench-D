@custom_derivatives.custom_jvp
@jit
@implements(osp_special.expi, module='scipy.special')
def expi(x: ArrayLike) -> Array:
  x_arr, = promote_args_inexact("expi", x)
  return jnp.piecewise(x_arr, [x_arr < 0], [_expi_neg, _expi_pos])
