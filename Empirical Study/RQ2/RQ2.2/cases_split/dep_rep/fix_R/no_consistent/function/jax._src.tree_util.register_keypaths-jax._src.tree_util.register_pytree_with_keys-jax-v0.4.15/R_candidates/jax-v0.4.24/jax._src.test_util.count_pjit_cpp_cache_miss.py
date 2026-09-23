@contextmanager
def count_pjit_cpp_cache_miss():
  original_pjit_lower = pjit_lib._pjit_lower
  count = [0]

  def pjit_lower_and_count(*args, **kwargs):
    count[0] += 1
    return original_pjit_lower(*args, **kwargs)

  pjit_lib._pjit_lower = pjit_lower_and_count
  try:
    yield count
  finally:
    pjit_lib._pjit_lower = original_pjit_lower
