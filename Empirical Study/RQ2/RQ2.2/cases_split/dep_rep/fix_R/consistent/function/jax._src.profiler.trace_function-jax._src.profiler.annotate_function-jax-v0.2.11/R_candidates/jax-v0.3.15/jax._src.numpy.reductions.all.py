@_wraps(np.all, skip_params=['out'])
def all(a, axis: Optional[Union[int, Tuple[int, ...]]] = None, out=None,
        keepdims=None, *, where=None):
  return _reduce_all(a, axis=_ensure_optional_axes(axis), out=out,
                     keepdims=keepdims, where=where)
