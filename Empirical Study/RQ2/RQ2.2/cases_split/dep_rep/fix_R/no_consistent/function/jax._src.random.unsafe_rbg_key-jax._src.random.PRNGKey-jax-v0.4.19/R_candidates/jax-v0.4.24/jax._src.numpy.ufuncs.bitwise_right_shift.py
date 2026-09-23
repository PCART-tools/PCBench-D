@implements(getattr(np, "bitwise_right_shift", np.right_shift), module='numpy')
@partial(jit, inline=True)
def bitwise_right_shift(x1: ArrayLike, x2: ArrayLike, /) -> Array:
  x1, x2 = promote_args_numeric("bitwise_right_shift", x1, x2)
  lax_fn = lax.shift_right_logical if \
    np.issubdtype(x1.dtype, np.unsignedinteger) else lax.shift_right_arithmetic
  return lax_fn(x1, x2)
