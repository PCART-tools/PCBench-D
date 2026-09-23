@implements(np.nanprod, skip_params=['out'])
@partial(api.jit, static_argnames=('axis', 'dtype', 'keepdims'))
def nanprod(a: ArrayLike, axis: Axis = None, dtype: DTypeLike | None = None, out: None = None,
            keepdims: bool = False, initial: ArrayLike | None = None,
            where: ArrayLike | None = None) -> Array:
  dtypes.check_user_dtype_supported(dtype, "nanprod")
  return _nan_reduction(a, 'nanprod', prod, 1, nan_if_all_nan=False,
                        axis=axis, dtype=dtype, out=out, keepdims=keepdims,
                        initial=initial, where=where)
