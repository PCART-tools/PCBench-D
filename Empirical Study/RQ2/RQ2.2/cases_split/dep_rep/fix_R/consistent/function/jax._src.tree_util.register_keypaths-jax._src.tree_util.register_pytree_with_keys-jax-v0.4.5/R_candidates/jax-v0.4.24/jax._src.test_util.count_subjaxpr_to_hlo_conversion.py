@contextmanager
def count_subjaxpr_to_hlo_conversion(fun_name: str):
  # No need to clear any caches since we generally jit and pmap fresh callables
  # in tests.

  mlir_lower = mlir.lower_jaxpr_to_fun
  count = [0]

  def mlir_lower_and_count(ctx, name, *args, **kwargs):
    if name == fun_name:
      count[0] += 1
    return mlir_lower(ctx, name, *args, **kwargs)

  mlir.lower_jaxpr_to_fun = mlir_lower_and_count
  try:
    yield count
  finally:
    mlir.lower_jaxpr_to_fun = mlir_lower
