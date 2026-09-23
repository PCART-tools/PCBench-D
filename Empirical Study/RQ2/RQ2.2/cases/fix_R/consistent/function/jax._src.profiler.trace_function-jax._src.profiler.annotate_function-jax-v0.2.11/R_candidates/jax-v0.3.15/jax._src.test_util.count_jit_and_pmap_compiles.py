@contextmanager
def count_jit_and_pmap_compiles():
  # No need to clear any caches since we generally jit and pmap fresh callables
  # in tests.

  mlir_jaxpr_subcomp = mlir.jaxpr_subcomp
  count = [0]

  def mlir_jaxpr_subcomp_and_count(*args, **kwargs):
    count[0] += 1
    return mlir_jaxpr_subcomp(*args, **kwargs)

  mlir.jaxpr_subcomp = mlir_jaxpr_subcomp_and_count
  try:
    yield count
  finally:
    mlir.jaxpr_subcomp = mlir_jaxpr_subcomp
