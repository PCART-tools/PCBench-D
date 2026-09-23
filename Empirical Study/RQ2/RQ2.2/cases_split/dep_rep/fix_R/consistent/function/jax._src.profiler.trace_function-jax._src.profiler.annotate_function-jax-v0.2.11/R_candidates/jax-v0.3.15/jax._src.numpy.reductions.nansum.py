@_wraps(np.nansum, skip_params=['out'])
@partial(api.jit, static_argnames=('axis', 'dtype', 'keepdims'))
def nansum(a, axis: Optional[Union[int, Tuple[int, ...]]] = None, dtype=None,
           out=None, keepdims=None, initial=None, where=None):
  lax_internal._check_user_dtype_supported(dtype, "nanprod")
  return _nan_reduction(a, 'nansum', sum, 0, nan_if_all_nan=False,
                        axis=axis, dtype=dtype, out=out, keepdims=keepdims,
                        initial=initial, where=where)
