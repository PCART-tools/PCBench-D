  def __iter__(self):
    if self.ndim == 0:
      raise TypeError("iteration over a 0-d array")  # same as numpy error
    else:
      assert self.is_fully_replicated or self.is_fully_addressable
      if dispatch.is_single_device_sharding(self.sharding) or self.is_fully_replicated:
        return (sl for chunk in self._chunk_iter(100) for sl in chunk._unstack())  # type: ignore
      elif isinstance(self.sharding, PmapSharding):
        return (self[i] for i in range(self.shape[0]))  # type: ignore
      else:
        # TODO(yashkatariya): Don't bounce to host and use `_chunk_iter` path
        # here after uneven partitioning support is added.
        return (api.device_put(self._value[i]) for i in range(self.shape[0]))
