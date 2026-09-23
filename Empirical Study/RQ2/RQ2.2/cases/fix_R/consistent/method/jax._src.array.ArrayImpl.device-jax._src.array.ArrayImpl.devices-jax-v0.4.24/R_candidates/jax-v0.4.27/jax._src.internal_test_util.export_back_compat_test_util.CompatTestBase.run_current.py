  def run_current(self, func: Callable, data: CompatTestData):
    """Lowers and runs the test function at the current JAX version."""
    return jax.jit(func)(*data.inputs)
