@_wraps(np.prod, skip_params=['out'])
def prod(a, axis: Optional[Union[int, Tuple[int, ...]]] = None, dtype=None,
         out=None, keepdims=None, initial=None, where=None):
  return _reduce_prod(a, axis=_ensure_optional_axes(axis), dtype=dtype,
                      out=out, keepdims=keepdims, initial=initial, where=where)
