def _rng_bit_generator_lowering(
    ctx, key, *, shape, dtype, algorithm):
  key_type = ir.RankedTensorType(key.type)
  key_shape, key_etype = key_type.shape, key_type.element_type
  # While the RngBitGenerator HLO accepts a u64[2] key on all backends, we
  # typically represent the key argument to this primitive as a u32[4] so as to
  # sidestep issues with the jax_enable_x64=False configuration. As a result, we
  # need to convert u32[4] -> u64[2] here in the translation rule. However, we
  # also polymorphically allow a u64[2] for backward compatibility.
  #
  # Separately, xops.RngBitGenerator doesn't support generating u8 or
  # u16, so we request u32 and truncate in that case.
  u32_type = ir.IntegerType.get_unsigned(32)
  u64_type = ir.IntegerType.get_unsigned(64)
  assert ((key_shape == [4] and key_etype == u32_type) or
          (key_shape == [2] and key_etype == u64_type)), (key_shape, key_etype)
  dtype = np.dtype(dtype)
  etype = mlir.dtype_to_ir_type(dtype)
  if dtype in (np.dtype('uint8'), np.dtype('uint16'), np.dtype('uint32'),
               np.dtype('uint64')):
    rbg_etype = etype
    rbg_dtype = dtype
  else:
    rbg_etype = u32_type
    rbg_dtype = np.uint32
  if key_etype == u32_type:
    key = hlo.BitcastConvertOp(
        ir.RankedTensorType.get([2], u64_type),
        hlo.ReshapeOp(ir.RankedTensorType.get([2, 2], u32_type), key)).result
  algorithm_attr = _rng_algorithm(algorithm)
  _, out_vals_aval = ctx.avals_out
  if any(not core.is_constant_shape(a.shape) for a in ctx.avals_out):
    output_shape = mlir.shape_tensor(
      mlir.eval_dynamic_shape(ctx, out_vals_aval.shape))
    out_key, out_vals = mlir.custom_call(
        "stablehlo.dynamic_rng_bit_generator",
        [key.type,
         mlir.aval_to_ir_type(core.ShapedArray(shape, rbg_dtype))],
        [key, output_shape],
        extra_attributes=dict(rng_algorithm=algorithm_attr)).results
  else:
    out_key, out_vals = hlo.RngBitGeneratorOp(
        key.type,
        ir.RankedTensorType.get(shape, rbg_etype),
        algorithm_attr, key).results
  if key_etype == u32_type:
    out_key = hlo.ReshapeOp(
        ir.RankedTensorType.get([4], u32_type),
        hlo.BitcastConvertOp(
            ir.RankedTensorType.get([2, 2], u32_type), out_key)).result
  if rbg_etype != etype:
    out_vals = hlo.ConvertOp(
      ir.RankedTensorType.get(ir.RankedTensorType(out_vals.type).shape, etype),
      out_vals).result
  return [out_key, out_vals]
