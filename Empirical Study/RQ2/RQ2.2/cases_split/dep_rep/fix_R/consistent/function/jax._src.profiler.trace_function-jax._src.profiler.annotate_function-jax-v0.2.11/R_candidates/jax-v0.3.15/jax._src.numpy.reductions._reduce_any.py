@partial(api.jit, static_argnames=('axis', 'keepdims'), inline=True)
def _reduce_any(a, axis: Optional[Union[int, Tuple[int, ...]]] = None, out=None,
                keepdims=None, *, where=None):
  return _reduction(a, "any", np.any, lax.bitwise_or, False, preproc=_cast_to_bool,
                    axis=axis, out=out, keepdims=keepdims, where_=where)
