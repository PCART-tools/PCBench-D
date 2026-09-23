  @implements(np.ufunc.outer, module="numpy.ufunc")
  @partial(jax.jit, static_argnums=[0])
  def outer(self, A: ArrayLike, B: ArrayLike, /, **kwargs) -> Array:
    if self.nin != 2:
      raise ValueError("outer only supported for binary ufuncs")
    if self.nout != 1:
      raise ValueError("outer only supported for functions returning a single value")
    check_arraylike(f"{self.__name__}.outer", A, B)
    _ravel = lambda A: jax.lax.reshape(A, (np.size(A),))
    result = jax.vmap(jax.vmap(partial(self._call, **kwargs), (None, 0)), (0, None))(_ravel(A), _ravel(B))
    return result.reshape(*np.shape(A), *np.shape(B))
