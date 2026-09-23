  def getTestCaseNames(self, testCaseClass):
    names = super().getTestCaseNames(testCaseClass)
    if _TEST_TARGETS.value:
      pattern = re.compile(_TEST_TARGETS.value)
      names = [name for name in names
               if pattern.search(f"{testCaseClass.__name__}.{name}")]
    if _EXCLUDE_TEST_TARGETS.value:
      pattern = re.compile(_EXCLUDE_TEST_TARGETS.value)
      names = [name for name in names
               if not pattern.search(f"{testCaseClass.__name__}.{name}")]
    return names
