@_wraps(np.any, skip_params=['out'])
def any(a, axis: Optional[Union[int, Tuple[int, ...]]] = None, out=None,
        keepdims=None, *, where=None):
  return _reduce_any(a, axis=_ensure_optional_axes(axis), out=out,
                     keepdims=keepdims, where=where)
