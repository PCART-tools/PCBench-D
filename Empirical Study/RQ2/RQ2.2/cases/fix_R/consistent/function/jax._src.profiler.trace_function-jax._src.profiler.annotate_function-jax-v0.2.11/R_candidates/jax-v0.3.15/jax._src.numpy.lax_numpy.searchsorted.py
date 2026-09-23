@_wraps(np.searchsorted, skip_params=['sorter'],
  extra_params=_dedent("""
    method : str
        One of 'scan' (default) or 'sort'. Controls the method used by the implementation; 'scan'
        tends to be more performant on CPU (particularly when ``a`` is very large), while
        'sort' is often more performant on accelerator backends like GPU and TPU (particularly
        when ``v`` is very large)."""))
@partial(jit, static_argnames=('side', 'sorter', 'method'))
def searchsorted(a, v, side='left', sorter=None, *, method='scan'):
  _check_arraylike("searchsorted", a, v)
  if side not in ['left', 'right']:
    raise ValueError(f"{side!r} is an invalid value for keyword 'side'. "
                     "Expected one of ['left', 'right'].")
  if method not in ['scan', 'sort']:
    raise ValueError(f"{method!r} is an invalid value for keyword 'method'. "
                     "Expected one of ['sort', 'scan'].")
  if sorter is not None:
    raise NotImplementedError("sorter is not implemented")
  if ndim(a) != 1:
    raise ValueError("a should be 1-dimensional")
  a, v = _promote_dtypes(a, v)
  dtype = int32 if len(a) <= np.iinfo(np.int32).max else int64
  if len(a) == 0:
    return zeros_like(v, dtype=dtype)
  impl = _searchsorted_via_scan if method == 'scan' else _searchsorted_via_sort
  return impl(a, v, side, dtype)
