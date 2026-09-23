@implements(np.left_shift, module='numpy')
@partial(jit, inline=True)
def left_shift(x: ArrayLike, y: ArrayLike, /) -> Array:
  return lax.shift_left(*promote_args_numeric("left_shift", x, y))
