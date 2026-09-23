  @contextmanager
  def assertNoWarnings(self):
    with warnings.catch_warnings():
      warnings.simplefilter("error")
      yield
