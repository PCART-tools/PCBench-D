  def __post_init__(self):
    if self.device_assignment is not None:
      assert isinstance(self.device_assignment, tuple)
      assert self.num_devices == len(self.device_assignment)
