@partial(api.jit, static_argnames=('axis', 'keepdims'), inline=True)
def _reduce_max(a: ArrayLike, axis: Axis = None, out: None = None,
                keepdims: bool = False, initial: ArrayLike | None = None,
                where: ArrayLike | None = None) -> Array:
  return _reduction(a, "max", np.max, lax.max, -np.inf, has_identity=False,
                    axis=axis, out=out, keepdims=keepdims,
                    initial=initial, where_=where, parallel_reduce=lax.pmax)
