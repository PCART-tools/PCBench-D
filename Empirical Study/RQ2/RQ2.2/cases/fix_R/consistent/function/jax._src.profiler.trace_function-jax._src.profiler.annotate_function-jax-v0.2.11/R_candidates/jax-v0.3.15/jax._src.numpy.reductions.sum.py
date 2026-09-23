@_wraps(np.sum, skip_params=['out'])
def sum(a, axis: Optional[Union[int, Tuple[int, ...]]] = None, dtype=None,
        out=None, keepdims=None, initial=None, where=None):
  return _reduce_sum(a, axis=_ensure_optional_axes(axis), dtype=dtype, out=out,
                     keepdims=keepdims, initial=initial, where=where)
