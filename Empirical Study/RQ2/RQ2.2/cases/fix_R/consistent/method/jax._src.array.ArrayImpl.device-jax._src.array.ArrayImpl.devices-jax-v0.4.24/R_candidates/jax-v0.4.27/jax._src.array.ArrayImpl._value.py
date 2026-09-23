  @property
  @functools.partial(profiler.annotate_function, name="np.asarray(jax.Array)")
  def _value(self) -> np.ndarray:
    self._check_if_deleted()

    if self._npy_value is None:
      if self.is_fully_replicated:
        self._npy_value = self._single_device_array_to_np_array()  # type: ignore
        self._npy_value.flags.writeable = False
        return cast(np.ndarray, self._npy_value)

      # TODO(yashkatariya): Merge `_process_has_full_value_in_mcjax` with
      # is_fully_addressable.
      if (not self.is_fully_addressable and
          not _process_has_full_value_in_mcjax(self.sharding, self.shape)):
        raise RuntimeError("Fetching value for `jax.Array` that spans "
                           "non-addressable devices is not possible. You can use "
                           "`jax.experimental.multihost_utils.process_allgather` "
                           "for this use case.")

      for i, _ in _cached_index_calc(self.sharding, self.shape):
        self._arrays[i]._copy_single_device_array_to_host_async()

      npy_value = np.empty(self.shape, self.dtype)
      for i, ind in _cached_index_calc(self.sharding, self.shape):
        npy_value[ind] = self._arrays[i]._single_device_array_to_np_array()
      self._npy_value = npy_value  # type: ignore
      self._npy_value.flags.writeable = False
    # https://docs.python.org/3/library/typing.html#typing.cast
    return cast(np.ndarray, self._npy_value)
