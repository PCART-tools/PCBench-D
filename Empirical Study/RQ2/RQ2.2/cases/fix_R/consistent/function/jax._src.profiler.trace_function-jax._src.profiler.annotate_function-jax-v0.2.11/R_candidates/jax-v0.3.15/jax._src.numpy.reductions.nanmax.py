@_wraps(np.nanmax, skip_params=['out'])
@partial(api.jit, static_argnames=('axis', 'keepdims'))
def nanmax(a, axis: Optional[Union[int, Tuple[int, ...]]] = None, out=None,
           keepdims=None, initial=None, where=None):
  return _nan_reduction(a, 'nanmax', max, -np.inf, nan_if_all_nan=initial is None,
                        axis=axis, out=out, keepdims=keepdims,
                        initial=initial, where=where)
