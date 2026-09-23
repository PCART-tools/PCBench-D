  @implements(np.ufunc.at, module="numpy.ufunc")
  @partial(jax.jit, static_argnums=[0], static_argnames=['inplace'])
  def at(self, a: ArrayLike, indices: Any, b: ArrayLike | None = None, /, *,
         inplace: bool = True) -> Array:
    if inplace:
      raise NotImplementedError(_AT_INPLACE_WARNING)
    if b is None:
      return self._at_via_scan(a, indices)
    else:
      return self._at_via_scan(a, indices, b)
