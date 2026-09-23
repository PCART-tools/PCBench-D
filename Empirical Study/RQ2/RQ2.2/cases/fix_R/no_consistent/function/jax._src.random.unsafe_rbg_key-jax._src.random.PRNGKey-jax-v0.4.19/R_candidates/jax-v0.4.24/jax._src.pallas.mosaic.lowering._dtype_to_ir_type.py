def _dtype_to_ir_type(dtype: jnp.dtype) -> ir.Type:
  if jnp.issubdtype(dtype, tpu_core.semaphore_dtype):
    if jnp.issubdtype(dtype, tpu_core.dma_semaphore):
      return ir.Type.parse("!tpu.dma_semaphore")
    elif jnp.issubdtype(dtype, tpu_core.semaphore):
      return ir.Type.parse("!tpu.semaphore")
    elif jnp.issubdtype(dtype, tpu_core.barrier_semaphore):
      return ir.Type.parse("!tpu.semaphore")
    else:
      raise NotImplementedError
  return mlir.dtype_to_ir_type(dtype)
