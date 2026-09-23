def _pgather_parallel_lowering(ctx, src, idx, *, axes):
  if any(not isinstance(axis, int) for axis in axes):
    raise NotImplementedError("pgather only supported in the SPMD lowering."
                              "Please open a feature request!")
  return mlir.lower_fun(_pgather_impl, multiple_results=False)(
      ctx, src, idx, axes=axes)
