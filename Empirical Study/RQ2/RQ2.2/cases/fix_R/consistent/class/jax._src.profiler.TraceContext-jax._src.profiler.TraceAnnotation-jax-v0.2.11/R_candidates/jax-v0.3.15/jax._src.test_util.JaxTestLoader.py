class JaxTestLoader(absltest.TestLoader):
  def getTestCaseNames(self, testCaseClass):
    names = super().getTestCaseNames(testCaseClass)
    if FLAGS.test_targets:
      pattern = re.compile(FLAGS.test_targets)
      names = [name for name in names
               if pattern.search(f"{testCaseClass.__name__}.{name}")]
    if FLAGS.exclude_test_targets:
      pattern = re.compile(FLAGS.exclude_test_targets)
      names = [name for name in names
               if not pattern.search(f"{testCaseClass.__name__}.{name}")]
    return names
