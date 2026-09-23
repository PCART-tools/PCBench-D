  def _at_via_scan(self, a: ArrayLike, indices: Any, *args: Any) -> Array:
    assert len(args) in {0, 1}
    check_arraylike(f"{self.__name__}.at", a, *args)
    dtype = jax.eval_shape(self._func, lax_internal._one(a), *(lax_internal._one(arg) for arg in args)).dtype
    a = lax_internal.asarray(a).astype(dtype)
    args = tuple(lax_internal.asarray(arg).astype(dtype) for arg in args)
    indices = _eliminate_deprecated_list_indexing(indices)
    if not indices:
      return a

    shapes = [np.shape(i) for i in indices if not isinstance(i, slice)]
    shape = shapes and jax.lax.broadcast_shapes(*shapes)
    if not shape:
      return a.at[indices].set(self._call(a.at[indices].get(), *args))

    if args:
      arg = _broadcast_to(args[0], (*shape, *args[0].shape[len(shape):]))
      args = (arg.reshape(math.prod(shape), *args[0].shape[len(shape):]),)
    indices = [idx if isinstance(idx, slice) else _broadcast_to(idx, shape).ravel() for idx in indices]

    def scan_fun(carry, x):
      i, a = carry
      idx = tuple(ind if isinstance(ind, slice) else ind[i] for ind in indices)
      a = a.at[idx].set(self._call(a.at[idx].get(), *(arg[i] for arg in args)))
      return (i + 1, a), x
    carry, _ = jax.lax.scan(scan_fun, (0, a), None, len(indices[0]))
    return carry[1]
