  def load_testdata_nested(self, testdata_nest) -> Iterable[CompatTestData]:
    # Load all the CompatTestData in a Python nest.
    if isinstance(testdata_nest, dict) and "testdata_version" in testdata_nest:
      yield self.load_testdata(testdata_nest)
    elif isinstance(testdata_nest, dict):
      for e in testdata_nest.values():
        yield from self.load_testdata_nested(e)
    elif isinstance(testdata_nest, list):
      for e in testdata_nest:
        yield from self.load_testdata_nested(e)
    else:
      assert False, testdata_nest
