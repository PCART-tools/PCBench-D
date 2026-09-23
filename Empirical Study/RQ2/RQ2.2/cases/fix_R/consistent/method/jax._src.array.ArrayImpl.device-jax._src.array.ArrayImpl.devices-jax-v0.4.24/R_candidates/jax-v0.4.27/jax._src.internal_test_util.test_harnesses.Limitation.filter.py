  def filter(self,
             device: str | None = None,
             dtype: DType | None = None) -> bool:
    """Check that a limitation is enabled for the given dtype and device."""
    return (self.enabled and
            (not self.dtypes or dtype is None or dtype in self.dtypes) and
            (device is None or device in self.devices))
