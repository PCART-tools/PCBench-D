@_wraps(np.deg2rad, module='numpy')
@partial(jit, inline=True)
def deg2rad(x):
  x, = _promote_args_inexact("deg2rad", x)
  return lax.mul(x, _lax_const(x, np.pi / 180))
