@contextmanager
def count_aot_jit_cpp_cache_miss():
  original_call = stages.Compiled.call
  count = [0]

  def compiled_call_count(*args, **kwargs):
    count[0] += 1
    return original_call(*args, **kwargs)

  stages.Compiled.call = compiled_call_count
  try:
    yield count
  finally:
    stages.Compiled.call = original_call
