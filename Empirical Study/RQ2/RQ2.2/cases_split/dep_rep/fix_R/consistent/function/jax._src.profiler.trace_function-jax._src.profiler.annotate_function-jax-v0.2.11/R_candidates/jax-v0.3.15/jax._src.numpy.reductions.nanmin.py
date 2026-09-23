@_wraps(np.nanmin, skip_params=['out'])
@partial(api.jit, static_argnames=('axis', 'keepdims'))
def nanmin(a, axis: Optional[Union[int, Tuple[int, ...]]] = None, out=None,
           keepdims=None, initial=None, where=None):
  return _nan_reduction(a, 'nanmin', min, np.inf, nan_if_all_nan=initial is None,
                        axis=axis, out=out, keepdims=keepdims,
                        initial=initial, where=where)
