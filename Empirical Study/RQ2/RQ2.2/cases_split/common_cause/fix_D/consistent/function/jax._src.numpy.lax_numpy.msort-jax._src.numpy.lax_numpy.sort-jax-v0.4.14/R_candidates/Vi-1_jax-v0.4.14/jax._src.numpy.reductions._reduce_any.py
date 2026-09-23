@partial(api.jit, static_argnames=('axis', 'keepdims'), inline=True)
def _reduce_any(a: ArrayLike, axis: Axis = None, out: None = None,
                keepdims: bool = False, *, where: Optional[ArrayLike] = None) -> Array:
  return _reduction(a, "any", np.any, lax.bitwise_or, False, preproc=_cast_to_bool,
                    axis=axis, out=out, keepdims=keepdims, where_=where)
