@partial(api.jit, static_argnames=('axis', 'dtype', 'keepdims', 'promote_integers'), inline=True)
def _reduce_prod(a: ArrayLike, axis: Axis = None, dtype: DTypeLike | None = None,
                 out: None = None, keepdims: bool = False,
                 initial: ArrayLike | None = None, where: ArrayLike | None = None,
                 promote_integers: bool = True) -> Array:
  return _reduction(a, "prod", np.prod, lax.mul, 1, preproc=_cast_to_numeric,
                    bool_op=lax.bitwise_and, upcast_f16_for_computation=True,
                    axis=axis, dtype=dtype, out=out, keepdims=keepdims,
                    initial=initial, where_=where, promote_integers=promote_integers)
