@partial(jit, static_argnames=('side', 'method'))
def searchsorted(a: ArrayLike, v: ArrayLike, side: str = 'left',
                 sorter: ArrayLike | None = None, *, method: str = 'scan') -> Array:
  """Perform a binary search within a sorted array.

  JAX implementation of :func:`numpy.searchsorted`.

  This will return the indices within a sorted array ``a`` where values in ``v``
  can be inserted to maintain its sort order.

  Args:
    a: one-dimensional array, assumed to be in sorted order unless ``sorter`` is specified.
    v: N-dimensional array of query values
    side: ``'left'`` (default) or ``'right'``; specifies whether insertion indices will be
      to the left or the right in case of ties.
    sorter: optional array of indices specifying the sort order of ``a``. If specified,
      then the algorithm assumes that ``a[sorter]`` is in sorted order.
    method: one of ``'scan'`` (default), ``'scan_unrolled'``, ``'sort'`` or ``'compare_all'``.
      See *Note* below.

  Returns:
    Array of insertion indices of shape ``v.shape``.

  Note:
    The ``method`` argument controls the algorithm used to compute the insertion indices.

    - ``'scan'`` (the default) tends to be more performant on CPU, particularly when ``a`` is
      very large.
    - ``'scan_unrolled'`` is more performant on GPU at the expense of additional compile time.
    - ``'sort'`` is often more performant on accelerator backends like GPU and TPU, particularly
      when ``v`` is very large.
    - ``'compare_all'`` tends to be the most performant when ``a`` is very small.

  Examples:
    Searching for a single value:

    >>> a = jnp.array([1, 2, 2, 3, 4, 5, 5])
    >>> jnp.searchsorted(a, 2)
    Array(1, dtype=int32)
    >>> jnp.searchsorted(a, 2, side='right')
    Array(3, dtype=int32)

    Searching for a batch of values:

    >>> vals = jnp.array([0, 3, 8, 1.5, 2])
    >>> jnp.searchsorted(a, vals)
    Array([0, 3, 7, 1, 1], dtype=int32)

    Optionally, the ``sorter`` argument can be used to find insertion indices into
    an array sorted via :func:`jax.numpy.argsort`:

    >>> a = jnp.array([4, 3, 5, 1, 2])
    >>> sorter = jnp.argsort(a)
    >>> jnp.searchsorted(a, vals, sorter=sorter)
    Array([0, 2, 5, 1, 1], dtype=int32)

    The result is equivalent to passing the sorted array:

    >>> jnp.searchsorted(jnp.sort(a), vals)
    Array([0, 2, 5, 1, 1], dtype=int32)
  """
  if sorter is None:
    util.check_arraylike("searchsorted", a, v)
  else:
    util.check_arraylike("searchsorted", a, v, sorter)
  if side not in ['left', 'right']:
    raise ValueError(f"{side!r} is an invalid value for keyword 'side'. "
                     "Expected one of ['left', 'right'].")
  if method not in ['scan', 'scan_unrolled', 'sort', 'compare_all']:
    raise ValueError(
        f"{method!r} is an invalid value for keyword 'method'. "
        "Expected one of ['sort', 'scan', 'scan_unrolled', 'compare_all'].")
  if ndim(a) != 1:
    raise ValueError("a should be 1-dimensional")
  a, v = util.promote_dtypes(a, v)
  if sorter is not None:
    a = a[sorter]
  dtype = int32 if len(a) <= np.iinfo(np.int32).max else int64
  if len(a) == 0:
    return zeros_like(v, dtype=dtype)
  impl = {
      'scan': partial(_searchsorted_via_scan, False),
      'scan_unrolled': partial(_searchsorted_via_scan, True),
      'sort': _searchsorted_via_sort,
      'compare_all': _searchsorted_via_compare_all,
  }[method]
  return impl(asarray(a), asarray(v), side, dtype)  # type: ignore
