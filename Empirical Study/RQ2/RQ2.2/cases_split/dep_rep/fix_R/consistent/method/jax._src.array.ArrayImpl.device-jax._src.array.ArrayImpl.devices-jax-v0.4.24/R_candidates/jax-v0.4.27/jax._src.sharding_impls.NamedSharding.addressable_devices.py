  @property
  def addressable_devices(self) -> set[Device]:
    # Override addressable devices because there is a high chance that the mesh
    # across multiple NamedSharding objects will be the same.
    return self.mesh._local_devices_set
