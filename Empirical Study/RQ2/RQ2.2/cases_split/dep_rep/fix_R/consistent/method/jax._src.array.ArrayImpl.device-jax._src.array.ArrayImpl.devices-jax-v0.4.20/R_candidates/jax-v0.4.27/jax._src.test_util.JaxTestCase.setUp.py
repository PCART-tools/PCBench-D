  def setUp(self):
    super().setUp()
    self._original_config = {}
    for key, value in self._default_config.items():
      self._original_config[key] = config._read(key)
      config.update(key, value)

    # We use the adler32 hash for two reasons.
    # a) it is deterministic run to run, unlike hash() which is randomized.
    # b) it returns values in int32 range, which RandomState requires.
    self._rng = npr.RandomState(zlib.adler32(self._testMethodName.encode()))
