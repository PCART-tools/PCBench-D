@implements(osp_special.exp1, module="scipy.special")
def exp1(x: ArrayLike, module='scipy.special') -> Array:
  x, = promote_args_inexact("exp1", x)
  # Casting because custom_jvp generic does not work correctly with mypy.
  return cast(Array, expn(1, x))
