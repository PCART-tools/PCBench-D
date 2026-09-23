def _empty_lower(ctx, *, dtype):
  dtype = dtype if dtypes.issubdtype(dtype, dtypes.extended) else np.dtype(dtype)
  phys_aval = core.physical_aval(core.ShapedArray((), dtype))
  return mlir.ir_constants(np.zeros(phys_aval.shape, phys_aval.dtype))
