  @functools.cached_property
  def addressable_devices(self) -> set[Device]:
    """The set of devices in the :class:`Sharding` that are addressable by the
       current process.
    """
    # Add a fast path for single controller runtimes.
    if xb.process_count() == 1:
      return self.device_set
    return {d for d in self.device_set
            if d.process_index == d.client.process_index()}
