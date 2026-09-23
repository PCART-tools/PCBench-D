def aval_to_ir_type(aval, shape=None, memory_space: TPUMemorySpace | None = None):
  if shape is None:
    shape = aval.shape
  if isinstance(aval, state.AbstractRef):
    memspace = _memory_space_to_tpu_memspace(memory_space)
    return ir.MemRefType.get(shape, mlir.dtype_to_ir_type(aval.dtype),
                             memory_space=memspace)
  elif isinstance(aval, jax_core.ShapedArray):
    if shape == ():
      return mlir.dtype_to_ir_type(aval.dtype)
    return ir.VectorType.get(shape, mlir.dtype_to_ir_type(aval.dtype))
  raise NotImplementedError(aval)
