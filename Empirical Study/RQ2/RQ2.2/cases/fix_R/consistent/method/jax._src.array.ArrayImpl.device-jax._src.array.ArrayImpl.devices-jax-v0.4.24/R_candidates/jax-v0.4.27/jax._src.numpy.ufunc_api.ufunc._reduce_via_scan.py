  def _reduce_via_scan(self, arr: ArrayLike, axis: int = 0, dtype: DTypeLike | None = None,
                       keepdims: bool = False, initial: ArrayLike | None = None,
                       where: ArrayLike | None = None) -> Array:
    assert self.nin == 2 and self.nout == 1
    arr = lax_internal.asarray(arr)
    if initial is None:
      initial = self.identity
    if dtype is None:
      dtype = jax.eval_shape(self._func, lax_internal._one(arr), lax_internal._one(arr)).dtype
    if where is not None:
      where = _broadcast_to(where, arr.shape)
    if isinstance(axis, tuple):
      axis = tuple(canonicalize_axis(a, arr.ndim) for a in axis)
      raise NotImplementedError("tuple of axes")
    elif axis is None:
      if keepdims:
        final_shape = (1,) * arr.ndim
      else:
        final_shape = ()
      arr = arr.ravel()
      if where is not None:
        where = where.ravel()
      axis = 0
    else:
      axis = canonicalize_axis(axis, arr.ndim)
      if keepdims:
        final_shape = (*arr.shape[:axis], 1, *arr.shape[axis + 1:])
      else:
        final_shape = (*arr.shape[:axis], *arr.shape[axis + 1:])

    # TODO: handle without transpose?
    if axis != 0:
      arr = _moveaxis(arr, axis, 0)
      if where is not None:
        where = _moveaxis(where, axis, 0)

    if initial is None and arr.shape[0] == 0:
      raise ValueError("zero-size array to reduction operation {self.__name__} which has no ideneity")

    def body_fun(i, val):
      if where is None:
        return self._call(val, arr[i].astype(dtype))
      else:
        return _where(where[i], self._call(val, arr[i].astype(dtype)), val)

    start_value: ArrayLike
    if initial is None:
      start_index = 1
      start_value = arr[0]
    else:
      start_index = 0
      start_value = initial
    start_value = _broadcast_to(lax_internal.asarray(start_value).astype(dtype), arr.shape[1:])

    result = jax.lax.fori_loop(start_index, arr.shape[0], body_fun, start_value)

    if keepdims:
      result = result.reshape(final_shape)
    return result
