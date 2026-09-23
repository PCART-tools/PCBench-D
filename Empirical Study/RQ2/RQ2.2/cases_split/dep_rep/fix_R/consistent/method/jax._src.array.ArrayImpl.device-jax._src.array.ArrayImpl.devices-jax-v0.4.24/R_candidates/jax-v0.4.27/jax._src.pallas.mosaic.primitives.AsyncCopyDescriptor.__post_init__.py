  def __post_init__(self):
    if (self.src_sem is None) ^ (self.device_id is None):
      raise ValueError("Either both or neither `src_sem` and `device_id` "
                       "can be set.")
