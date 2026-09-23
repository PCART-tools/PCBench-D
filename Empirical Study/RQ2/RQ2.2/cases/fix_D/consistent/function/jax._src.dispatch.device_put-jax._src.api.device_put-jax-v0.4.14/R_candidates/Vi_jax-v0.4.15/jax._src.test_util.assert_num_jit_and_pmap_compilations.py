@contextmanager
def assert_num_jit_and_pmap_compilations(times):
  with count_jit_and_pmap_compiles() as count:
    yield
  if count[0] != times:
    raise AssertionError(f"Expected exactly {times} XLA compilations, "
                         f"but executed {count[0]}")
