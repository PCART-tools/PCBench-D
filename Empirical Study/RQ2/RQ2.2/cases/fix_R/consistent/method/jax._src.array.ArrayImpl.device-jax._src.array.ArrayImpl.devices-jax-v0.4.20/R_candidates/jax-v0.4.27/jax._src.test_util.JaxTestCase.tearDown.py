  def tearDown(self):
    for key, value in self._original_config.items():
      config.update(key, value)
    super().tearDown()
