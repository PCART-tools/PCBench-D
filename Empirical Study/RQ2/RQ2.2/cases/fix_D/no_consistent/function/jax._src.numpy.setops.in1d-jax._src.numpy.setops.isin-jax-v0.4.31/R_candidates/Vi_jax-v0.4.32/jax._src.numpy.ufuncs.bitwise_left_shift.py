@implements(getattr(np, "bitwise_left_shift", np.left_shift), module='numpy')
@partial(jit, inline=True)
def bitwise_left_shift(x: ArrayLike, y: ArrayLike, /) -> Array:
  return lax.shift_left(*promote_args_numeric("bitwise_left_shift", x, y))
