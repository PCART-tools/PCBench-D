@partial(api.jit, static_argnames=('axis', 'keepdims'), inline=True)
def _reduce_min(a: ArrayLike, axis: Axis = None, out: None = None,
                keepdims: bool = False, initial: Optional[ArrayLike] = None,
                where: Optional[ArrayLike] = None) -> Array:
  return _reduction(a, "min", np.min, lax.min, np.inf, has_identity=False,
                    axis=axis, out=out, keepdims=keepdims,
                    initial=initial, where_=where, parallel_reduce=lax.pmin)
