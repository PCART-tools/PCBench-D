  def _reduceat_via_scan(self, a: ArrayLike, indices: Any, axis: int = 0,
                         dtype: DTypeLike | None = None) -> Array:
    check_arraylike(f"{self.__name__}.reduceat", a, indices)
    a = lax_internal.asarray(a)
    idx_tuple = _eliminate_deprecated_list_indexing(indices)
    assert len(idx_tuple) == 1
    indices = idx_tuple[0]
    if a.ndim == 0:
      raise ValueError(f"reduceat: a must have 1 or more dimension, got {a.shape=}")
    if indices.ndim != 1:
      raise ValueError(f"reduceat: indices must be one-dimensional, got {indices.shape=}")
    if dtype is None:
      dtype = a.dtype
    if axis is None or isinstance(axis, (tuple, list)):
      raise ValueError("reduceat requires a single integer axis.")
    axis = canonicalize_axis(axis, a.ndim)
    out = take(a, indices, axis=axis)
    ind = jax.lax.expand_dims(append(indices, a.shape[axis]),
                              list(np.delete(np.arange(out.ndim), axis)))
    ind_start = jax.lax.slice_in_dim(ind, 0, ind.shape[axis] - 1, axis=axis)
    ind_end = jax.lax.slice_in_dim(ind, 1, ind.shape[axis], axis=axis)
    def loop_body(i, out):
      return _where((i > ind_start) & (i < ind_end),
                    self._call(out, take(a, jax.lax.expand_dims(i, (0,)), axis=axis)),
                    out)
    return jax.lax.fori_loop(0, a.shape[axis], loop_body, out)
