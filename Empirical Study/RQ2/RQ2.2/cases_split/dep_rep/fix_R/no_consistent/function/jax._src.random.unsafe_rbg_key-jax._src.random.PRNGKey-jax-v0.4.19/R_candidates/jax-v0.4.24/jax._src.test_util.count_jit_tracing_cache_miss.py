@contextmanager
def count_jit_tracing_cache_miss():
  original_create_pjit_jaxpr = pjit_lib._create_pjit_jaxpr
  count = [0]

  @lu.cache
  def create_pjit_jaxpr_and_count(*args):
    count[0] += 1
    return original_create_pjit_jaxpr(*args)

  pjit_lib._create_pjit_jaxpr = create_pjit_jaxpr_and_count
  try:
    yield count
  finally:
    pjit_lib._create_pjit_jaxpr = original_create_pjit_jaxpr
