def _dot_general_lower(ctx, lhs, rhs, *, dimension_numbers,
                       precision, preferred_element_type: np.dtype | None,
                       platform: str = "default"):
  del preferred_element_type  # Implied by the output aval
  lhs_aval, rhs_aval = ctx.avals_in
  lhs_dtype, rhs_dtype = lhs_aval.dtype, rhs_aval.dtype
  aval_out, = ctx.avals_out
  (lhs_contracting, rhs_contracting), (lhs_batch, rhs_batch) = dimension_numbers

  # TODO(b/...): JAX's dot_general primitive accepts the same input dtype
  # combinations that are accepted in XLA's shape_inference.cc (the canonical
  # reference for the HLO type system), but actually different XLA platforms
  # fail on codegen for different accepted cases. To handle those cases, we
  # insert ConvertOps on the input, in a platform-dependent way.
  if lhs_dtype != rhs_dtype:
    if platform == "tpu":
      handled = lambda dt: (dtypes.issubdtype(dt, np.floating) or
                            dtypes.issubdtype(dt, np.integer))
      if not (handled(lhs_dtype) and handled(rhs_dtype)):
        lhs = mlir.convert_hlo(ctx, lhs, lhs_aval,
                               core.ShapedArray(lhs_aval.shape, aval_out.dtype))
        rhs = mlir.convert_hlo(ctx, rhs, rhs_aval,
                               core.ShapedArray(rhs_aval.shape, aval_out.dtype))
        lhs_dtype = rhs_dtype = aval_out.dtype
    else:  # cpu and gpu
      lhs = mlir.convert_hlo(ctx, lhs, lhs_aval,
                             core.ShapedArray(lhs_aval.shape, aval_out.dtype))
      rhs = mlir.convert_hlo(ctx, rhs, rhs_aval,
                             core.ShapedArray(rhs_aval.shape, aval_out.dtype))
      lhs_dtype = rhs_dtype = aval_out.dtype

  # TODO(b/195364460): Work around slow XLA/CPU implementation of float16 matmul
  if platform == "cpu":
    if lhs_dtype == np.float16:
      lhs = mlir.convert_hlo(ctx, lhs, lhs_aval,
                             core.ShapedArray(lhs_aval.shape, np.float32))

    if rhs_dtype == np.float16:
      rhs = mlir.convert_hlo(ctx, rhs, rhs_aval,
                             core.ShapedArray(rhs_aval.shape, np.float32))


  dot_dnums = hlo.DotDimensionNumbers.get(
      lhs_batching_dimensions=list(lhs_batch),
      rhs_batching_dimensions=list(rhs_batch),
      lhs_contracting_dimensions=list(lhs_contracting),
      rhs_contracting_dimensions=list(rhs_contracting))
  return [
      hlo.dot_general(
          mlir.aval_to_ir_type(aval_out),
          lhs,
          rhs,
          dot_dnums,
          precision_config=precision_attr(precision))
  ]
