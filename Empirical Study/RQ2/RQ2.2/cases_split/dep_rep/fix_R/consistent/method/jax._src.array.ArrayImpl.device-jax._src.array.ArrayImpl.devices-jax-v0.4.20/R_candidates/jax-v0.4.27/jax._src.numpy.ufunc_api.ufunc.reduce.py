  @implements(np.ufunc.reduce, module="numpy.ufunc")
  @partial(jax.jit, static_argnames=['self', 'axis', 'dtype', 'out', 'keepdims'])
  def reduce(self, a: ArrayLike, axis: int = 0, dtype: DTypeLike | None = None,
             out: None = None, keepdims: bool = False, initial: ArrayLike | None = None,
             where: ArrayLike | None = None) -> Array:
    check_arraylike(f"{self.__name__}.reduce", a)
    if self.nin != 2:
      raise ValueError("reduce only supported for binary ufuncs")
    if self.nout != 1:
      raise ValueError("reduce only supported for functions returning a single value")
    if out is not None:
      raise NotImplementedError(f"out argument of {self.__name__}.reduce()")
    if initial is not None:
      check_arraylike(f"{self.__name__}.reduce", initial)
    if where is not None:
      check_arraylike(f"{self.__name__}.reduce", where)
      if self.identity is None and initial is None:
        raise ValueError(f"reduction operation {self.__name__!r} does not have an identity, "
                         "so to use a where mask one has to specify 'initial'.")
      if lax_internal._dtype(where) != bool:
        raise ValueError(f"where argument must have dtype=bool; got dtype={lax_internal._dtype(where)}")
    primitive = get_if_single_primitive(self._call, *(self.nin * [lax_internal._one(a)]))
    if primitive is None:
      reducer = self._reduce_via_scan
    else:
      reducer = _primitive_reducers.get(primitive, self._reduce_via_scan)
    return reducer(a, axis=axis, dtype=dtype, keepdims=keepdims, initial=initial, where=where)
