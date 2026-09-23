@partial(api.jit, static_argnames=('axis', 'keepdims'), inline=True)
def _reduce_min(a, axis: Optional[Union[int, Tuple[int, ...]]] = None, out=None,
                keepdims=None, initial=None, where=None):
  return _reduction(a, "min", np.min, lax.min, np.inf, has_identity=False,
                    axis=axis, out=out, keepdims=keepdims,
                    initial=initial, where_=where, parallel_reduce=lax.pmin)
