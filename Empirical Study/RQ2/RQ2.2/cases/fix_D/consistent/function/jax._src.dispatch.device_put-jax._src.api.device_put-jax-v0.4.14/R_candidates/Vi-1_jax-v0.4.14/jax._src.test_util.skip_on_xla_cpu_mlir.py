def skip_on_xla_cpu_mlir(test_method):
  """A decorator to skip tests when MLIR lowering is enabled."""
  @functools.wraps(test_method)
  def test_method_wrapper(self, *args, **kwargs):
    xla_flags = os.getenv('XLA_FLAGS') or ''
    if '--xla_cpu_use_xla_runtime' in xla_flags:
      test_name = getattr(test_method, '__name__', '[unknown test]')
      raise unittest.SkipTest(
          f'{test_name} not supported on XLA:CPU MLIR')
    return test_method(self, *args, **kwargs)
  return test_method_wrapper
