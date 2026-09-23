  def load_testdata(self, testdata_dict: dict[str, Any]) -> CompatTestData:
    if testdata_dict["testdata_version"] == CURRENT_TESTDATA_VERSION:
      return CompatTestData(**testdata_dict)
    else:
      raise NotImplementedError("testdata_version not recognized: " +
                                testdata_dict["testdata_version"])
