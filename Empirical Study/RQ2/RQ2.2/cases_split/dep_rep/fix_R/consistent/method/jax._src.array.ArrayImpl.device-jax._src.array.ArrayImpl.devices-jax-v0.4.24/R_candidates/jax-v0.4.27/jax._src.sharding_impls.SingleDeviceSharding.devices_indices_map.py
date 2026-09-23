  def devices_indices_map(self, global_shape: Shape) -> Mapping[Device, Index]:  # type: ignore
    return {self._device: (slice(None),) * len(global_shape)}
