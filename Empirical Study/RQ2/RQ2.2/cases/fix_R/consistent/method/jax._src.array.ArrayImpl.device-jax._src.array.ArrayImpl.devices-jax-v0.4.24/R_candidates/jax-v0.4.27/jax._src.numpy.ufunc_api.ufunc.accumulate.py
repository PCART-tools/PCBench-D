  @implements(np.ufunc.accumulate, module="numpy.ufunc")
  @partial(jax.jit, static_argnames=['self', 'axis', 'dtype'])
  def accumulate(self, a: ArrayLike, axis: int = 0, dtype: DTypeLike | None = None,
                 out: None = None) -> Array:
    if self.nin != 2:
      raise ValueError("accumulate only supported for binary ufuncs")
    if self.nout != 1:
      raise ValueError("accumulate only supported for functions returning a single value")
    if out is not None:
      raise NotImplementedError(f"out argument of {self.__name__}.accumulate()")
    primitive = get_if_single_primitive(self._call, *(self.nin * [lax_internal._one(a)]))
    if primitive is None:
      accumulator = self._accumulate_via_scan
    else:
      accumulator = _primitive_accumulators.get(primitive, self._accumulate_via_scan)
    return accumulator(a, axis=axis, dtype=dtype)
