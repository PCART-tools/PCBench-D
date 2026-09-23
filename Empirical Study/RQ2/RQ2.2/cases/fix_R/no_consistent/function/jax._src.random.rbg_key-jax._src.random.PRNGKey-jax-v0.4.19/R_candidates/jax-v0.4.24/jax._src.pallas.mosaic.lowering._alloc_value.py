def _alloc_value(aval: jax_core.AbstractValue) -> ir.Value:
  if isinstance(aval, pl_core.AbstractMemoryRef):
    memspace = ir.Attribute.parse(f"#tpu.memory_space<{aval.memory_space}>")
    if jnp.issubdtype(aval.dtype, tpu_core.semaphore_dtype):
      assert aval.memory_space == TPUMemorySpace.SEMAPHORE
      memref_type = aval_to_ir_type(aval, memory_space=TPUMemorySpace.SEMAPHORE)
      return tpu.AllocaSemaphoreOp(memref_type).result
    else:
      out_type = ir.MemRefType.get(
          aval.shape, _dtype_to_ir_type(aval.dtype), memory_space=memspace)
      return memref.AllocaOp(out_type, [], []).result
  elif isinstance(aval, tpu_core.AbstractSemaphore):
    memref_type = aval_to_ir_type(aval, memory_space=TPUMemorySpace.SEMAPHORE)
    return tpu.AllocaSemaphoreOp(memref_type).result
  raise NotImplementedError(f"Cannot allocate {type(aval)}.")
