@partial(api.jit, static_argnames=('axis', 'keepdims'), inline=True)
def _reduce_all(a: ArrayLike, axis: Axis = None, out: None = None,
                keepdims: bool = False, *, where: ArrayLike | None = None) -> Array:
  return _reduction(a, "all", np.all, lax.bitwise_and, True, preproc=_cast_to_bool,
                    axis=axis, out=out, keepdims=keepdims, where_=where)
