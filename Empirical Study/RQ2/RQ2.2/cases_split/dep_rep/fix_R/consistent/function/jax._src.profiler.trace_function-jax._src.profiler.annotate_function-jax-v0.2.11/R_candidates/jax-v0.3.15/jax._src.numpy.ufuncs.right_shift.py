@_wraps(np.right_shift, module='numpy')
@partial(jit, inline=True)
def right_shift(x1, x2):
  x1, x2 = _promote_args(np.right_shift.__name__, x1, x2)
  lax_fn = lax.shift_right_logical if \
    np.issubdtype(x1.dtype, np.unsignedinteger) else lax.shift_right_arithmetic
  return lax_fn(x1, x2)
