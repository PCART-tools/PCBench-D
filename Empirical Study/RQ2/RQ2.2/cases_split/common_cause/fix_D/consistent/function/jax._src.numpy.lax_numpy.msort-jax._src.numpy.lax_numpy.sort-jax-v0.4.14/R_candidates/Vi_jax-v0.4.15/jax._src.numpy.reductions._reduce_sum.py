@partial(api.jit, static_argnames=('axis', 'dtype', 'keepdims', 'promote_integers'), inline=True)
def _reduce_sum(a: ArrayLike, axis: Axis = None, dtype: DTypeLike = None,
                out: None = None, keepdims: bool = False,
                initial: Optional[ArrayLike] = None, where: Optional[ArrayLike] = None,
                promote_integers: bool = True) -> Array:
  return _reduction(a, "sum", np.sum, lax.add, 0, preproc=_cast_to_numeric,
                    bool_op=lax.bitwise_or, upcast_f16_for_computation=True,
                    axis=axis, dtype=dtype, out=out, keepdims=keepdims,
                    initial=initial, where_=where, parallel_reduce=lax.psum,
                    promote_integers=promote_integers)
