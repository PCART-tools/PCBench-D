@contextmanager
def count_primitive_compiles():
  dispatch.xla_primitive_callable.cache_clear()

  count = [-1]
  try:
    yield count
  finally:
    count[0] = dispatch.xla_primitive_callable.cache_info().misses
