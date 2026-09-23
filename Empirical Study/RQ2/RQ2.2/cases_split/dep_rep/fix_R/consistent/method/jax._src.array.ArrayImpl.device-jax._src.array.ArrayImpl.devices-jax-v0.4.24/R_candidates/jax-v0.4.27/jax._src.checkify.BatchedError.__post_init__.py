  def __post_init__(self):
    traceback_info = list(self.error_mapping.values())[0].traceback_info
    super().__init__(traceback_info)
