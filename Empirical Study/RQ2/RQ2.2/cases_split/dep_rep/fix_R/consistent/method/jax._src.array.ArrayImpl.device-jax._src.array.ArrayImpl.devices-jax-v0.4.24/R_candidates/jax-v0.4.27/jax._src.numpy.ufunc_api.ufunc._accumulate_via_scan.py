  def _accumulate_via_scan(self, arr: ArrayLike, axis: int = 0,
                           dtype: DTypeLike | None = None) -> Array:
    assert self.nin == 2 and self.nout == 1
    check_arraylike(f"{self.__name__}.accumulate", arr)
    arr = lax_internal.asarray(arr)

    if dtype is None:
      dtype = jax.eval_shape(self._func, lax_internal._one(arr), lax_internal._one(arr)).dtype

    if axis is None or isinstance(axis, tuple):
      raise ValueError("accumulate does not allow multiple axes")
    axis = canonicalize_axis(axis, np.ndim(arr))

    arr = _moveaxis(arr, axis, 0)
    def scan_fun(carry, _):
      i, x = carry
      y = _where(i == 0, arr[0].astype(dtype), self._call(x.astype(dtype), arr[i].astype(dtype)))
      return (i + 1, y), y
    _, result = jax.lax.scan(scan_fun, (0, arr[0].astype(dtype)), None, length=arr.shape[0])
    return _moveaxis(result, 0, axis)
