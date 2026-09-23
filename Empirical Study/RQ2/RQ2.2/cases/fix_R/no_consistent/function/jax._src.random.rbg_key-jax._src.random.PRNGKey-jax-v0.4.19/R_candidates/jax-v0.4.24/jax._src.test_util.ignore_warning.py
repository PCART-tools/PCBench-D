@contextmanager
def ignore_warning(*, message='', category=Warning, **kw):
  with warnings.catch_warnings():
    warnings.filterwarnings("ignore", message=message, category=category, **kw)
    yield
