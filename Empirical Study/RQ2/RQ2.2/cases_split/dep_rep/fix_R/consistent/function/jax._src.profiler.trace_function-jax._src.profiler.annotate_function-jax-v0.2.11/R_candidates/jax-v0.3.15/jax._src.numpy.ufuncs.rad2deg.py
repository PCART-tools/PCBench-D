@_wraps(np.rad2deg, module='numpy')
@partial(jit, inline=True)
def rad2deg(x):
  x, = _promote_args_inexact("rad2deg", x)
  return lax.mul(x, _lax_const(x, 180 / np.pi))
