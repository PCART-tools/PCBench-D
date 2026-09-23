@_wraps(np.min, skip_params=['out'])
def min(a, axis: Optional[Union[int, Tuple[int, ...]]] = None, out=None,
        keepdims=None, initial=None, where=None):
  return _reduce_min(a, axis=_ensure_optional_axes(axis), out=out,
                     keepdims=keepdims, initial=initial, where=where)
