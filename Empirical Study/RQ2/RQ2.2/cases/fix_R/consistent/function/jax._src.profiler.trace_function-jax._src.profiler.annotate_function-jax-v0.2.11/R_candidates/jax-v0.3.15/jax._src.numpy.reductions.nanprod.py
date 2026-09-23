@_wraps(np.nanprod, skip_params=['out'])
@partial(api.jit, static_argnames=('axis', 'dtype', 'keepdims'))
def nanprod(a, axis: Optional[Union[int, Tuple[int, ...]]] = None, dtype=None,
            out=None, keepdims=None, initial=None, where=None):
  lax_internal._check_user_dtype_supported(dtype, "nanprod")
  return _nan_reduction(a, 'nanprod', prod, 1, nan_if_all_nan=False,
                        axis=axis, dtype=dtype, out=out, keepdims=keepdims,
                        initial=initial, where=where)
