def isdtype(dtype: DTypeLike, kind: str | DType | tuple[str | DType]) -> bool:
  """Returns a boolean indicating whether a provided dtype is of a specified kind.

  Args:
    dtype : the input dtype
    kind : the data type kind.
      If ``kind`` is dtype-like, return ``dtype = kind``.
      If ``kind`` is a string, then return True if the dtype is in the specified category:

      - ``'bool'``: ``{bool}``
      - ``'signed integer'``: ``{int4, int8, int16, int32, int64}``
      - ``'unsigned integer'``: ``{uint4, uint8, uint16, uint32, uint64}``
      - ``'integral'``: shorthand for ``('signed integer', 'unsigned integer')``
      - ``'real floating'``: ``{float8_*, float16, bfloat16, float32, float64}``
      - ``'complex floating'``: ``{complex64, complex128}``
      - ``'numeric'``: shorthand for ``('integral', 'real floating', 'complex floating')``

      If ``kind`` is a tuple, then return True if dtype matches any entry of the tuple.

  Returns:
    True or False
  """
  the_dtype = np.dtype(dtype)
  kind_tuple: tuple[DType | str] = kind if isinstance(kind, tuple) else (kind,)
  options: set[DType] = set()
  for kind in kind_tuple:
    if isinstance(kind, str):
      if kind not in _dtype_kinds:
        raise ValueError(f"Unrecognized {kind=} expected one of {list(_dtype_kinds.keys())}")
      options.update(_dtype_kinds[kind])
    elif isinstance(kind, np.dtype):
      options.add(kind)
    else:
      # TODO(jakevdp): should we handle scalar types or ScalarMeta here?
      raise TypeError(f"Expected kind to be a dtype, string, or tuple; got {kind=}")
  return the_dtype in options
