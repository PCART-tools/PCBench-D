@contextmanager
def count_jit_and_pmap_compiles():
  # No need to clear any caches since we generally jit and pmap fresh callables
  # in tests.

  mlir_lower = mlir.lower_jaxpr_to_module
  count = [0]

  def mlir_lower_and_count(*args, **kwargs):
    count[0] += 1
    return mlir_lower(*args, **kwargs)

  mlir.lower_jaxpr_to_module = mlir_lower_and_count
  try:
    yield count
  finally:
    mlir.lower_jaxpr_to_module = mlir_lower
