@partial(api.jit, static_argnames=('axis', 'dtype', 'keepdims'), inline=True)
def _reduce_sum(a, axis: Optional[Union[int, Tuple[int, ...]]] = None,
                dtype=None, out=None, keepdims=None, initial=None, where=None):
  return _reduction(a, "sum", np.sum, lax.add, 0,
                    bool_op=lax.bitwise_or, upcast_f16_for_computation=True,
                    axis=axis, dtype=dtype, out=out, keepdims=keepdims,
                    initial=initial, where_=where, parallel_reduce=lax.psum)
