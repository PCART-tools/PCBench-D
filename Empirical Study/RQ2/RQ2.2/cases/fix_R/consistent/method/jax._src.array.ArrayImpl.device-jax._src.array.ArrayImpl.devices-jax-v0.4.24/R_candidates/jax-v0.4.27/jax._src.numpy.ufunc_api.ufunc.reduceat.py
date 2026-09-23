  @implements(np.ufunc.reduceat, module="numpy.ufunc")
  @partial(jax.jit, static_argnames=['self', 'axis', 'dtype'])
  def reduceat(self, a: ArrayLike, indices: Any, axis: int = 0,
               dtype: DTypeLike | None = None, out: None = None) -> Array:
    if self.nin != 2:
      raise ValueError("reduceat only supported for binary ufuncs")
    if self.nout != 1:
      raise ValueError("reduceat only supported for functions returning a single value")
    if out is not None:
      raise NotImplementedError(f"out argument of {self.__name__}.reduceat()")
    return self._reduceat_via_scan(a, indices, axis=axis, dtype=dtype)
