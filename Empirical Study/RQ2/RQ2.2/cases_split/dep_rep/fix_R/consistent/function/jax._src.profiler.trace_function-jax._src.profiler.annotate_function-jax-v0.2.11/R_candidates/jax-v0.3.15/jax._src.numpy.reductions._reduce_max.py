@partial(api.jit, static_argnames=('axis', 'keepdims'), inline=True)
def _reduce_max(a, axis: Optional[Union[int, Tuple[int, ...]]] = None, out=None,
                keepdims=None, initial=None, where=None):
  return _reduction(a, "max", np.max, lax.max, -np.inf, has_identity=False,
                    axis=axis, out=out, keepdims=keepdims,
                    initial=initial, where_=where, parallel_reduce=lax.pmax)
