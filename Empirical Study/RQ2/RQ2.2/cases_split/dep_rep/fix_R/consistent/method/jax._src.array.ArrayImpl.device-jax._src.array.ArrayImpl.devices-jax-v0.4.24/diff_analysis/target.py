  def devices(self) -> set[Device]:
    self._check_if_deleted()
    return self.sharding.device_set
