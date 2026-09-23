@util._wraps(np.searchsorted, skip_params=['sorter'],
  extra_params=_dedent("""
    method : str
        One of 'scan' (default), 'sort' or 'compare_all'. Controls the method used by the
        implementation: 'scan' tends to be more performant on CPU (particularly when ``a`` is
        very large), 'sort' is often more performant on accelerator backends like GPU and TPU
        (particularly when ``v`` is very large), and 'compare_all' can be most performant
        when ``a`` is very small."""))
@partial(jit, static_argnames=('side', 'sorter', 'method'))
def searchsorted(a: ArrayLike, v: ArrayLike, side: str = 'left',
                 sorter: None = None, *, method: str = 'scan') -> Array:
  util.check_arraylike("searchsorted", a, v)
  if side not in ['left', 'right']:
    raise ValueError(f"{side!r} is an invalid value for keyword 'side'. "
                     "Expected one of ['left', 'right'].")
  if method not in ['scan', 'sort', 'compare_all']:
    raise ValueError(f"{method!r} is an invalid value for keyword 'method'. "
                     "Expected one of ['sort', 'scan', 'compare_all'].")
  if sorter is not None:
    raise NotImplementedError("sorter is not implemented")
  if ndim(a) != 1:
    raise ValueError("a should be 1-dimensional")
  a, v = util.promote_dtypes(a, v)
  dtype = int32 if len(a) <= np.iinfo(np.int32).max else int64
  if len(a) == 0:
    return zeros_like(v, dtype=dtype)
  impl = {
      'scan': _searchsorted_via_scan,
      'sort': _searchsorted_via_sort,
      'compare_all': _searchsorted_via_compare_all,
  }[method]
  return impl(asarray(a), asarray(v), side, dtype)
