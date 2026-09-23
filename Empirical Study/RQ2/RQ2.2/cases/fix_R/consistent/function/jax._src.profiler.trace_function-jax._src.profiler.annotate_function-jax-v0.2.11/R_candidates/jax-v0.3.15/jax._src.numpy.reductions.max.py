@_wraps(np.max, skip_params=['out'])
def max(a, axis: Optional[Union[int, Tuple[int, ...]]] = None, out=None,
        keepdims=None, initial=None, where=None):
  return _reduce_max(a, axis=_ensure_optional_axes(axis), out=out,
                     keepdims=keepdims, initial=initial, where=where)
