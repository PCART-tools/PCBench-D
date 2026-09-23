def _approx_top_k_lowering(ctx, operand, *, k,
                                  reduction_dimension, recall_target, is_max_k,
                                  reduction_input_size_override,
                                  aggregate_to_topk, fallback=False):
  assert ctx.avals_in
  assert all(isinstance(x, core.ShapedArray) for x in ctx.avals_in)

  op_shape = ctx.avals_in[0].shape
  if len(op_shape) == 0:
    raise ValueError(f'operand must be an array, but was {op_shape}')

  op_dims = op_shape
  op_type = mlir.dtype_to_ir_type(ctx.avals_in[0].dtype)
  recall_type = ir.F32Type.get()
  if reduction_dimension < 0:
    reduction_dimension = len(op_dims) + reduction_dimension

  comparator = _comparator_builder_mlir(ctx, op_type, is_max_k)
  iota = mlir.iota(ctx, core.ShapedArray(ctx.avals_in[0].shape, np.int32),
                   dimension=reduction_dimension)

  init_arg = hlo.ConstantOp(ir.DenseElementsAttr.get(np.int32(-1))).result
  # Can't write bf16 literals, so we write a f64 literal and convert it.
  init_val_literal = _get_init_val_literal(np.float64, is_max_k)
  init_val_array = np.array(init_val_literal, dtype=np.float64).reshape(())
  init_val = mlir.ir_constant(init_val_array)
  init_val = hlo.ConvertOp(ir.RankedTensorType.get([],
    mlir.dtype_to_ir_type(ctx.avals_in[0].dtype)), init_val).result

  backend_config = {
    "top_k" : mlir.i64_attr(k),
    "reduction_dim" : mlir.i64_attr(reduction_dimension),
    "recall_target" : mlir.ir.FloatAttr.get(recall_type, recall_target),
    "aggregate_to_topk" : mlir.ir.BoolAttr.get(aggregate_to_topk),
    "reduction_input_size_override" :
      mlir.i64_attr(reduction_input_size_override)}
  if fallback:
    backend_config["is_fallback"] = mlir.ir.BoolAttr.get(fallback)

  if xc.mlir_api_version >= 51:  # jaxlib >= 0.4.14
    if all(core.is_constant_shape(aval_out.shape) for aval_out in ctx.avals_out):
      result_shapes = None
    else:
      result_shapes = [
          mlir.shape_tensor(mlir.eval_dynamic_shape(ctx, aval_out.shape))
          for aval_out in ctx.avals_out]

    out = mlir.custom_call(
        "ApproxTopK",
        [mlir.aval_to_ir_type(aval) for aval in ctx.avals_out],
        [operand, iota, init_val, init_arg],
        called_computations=[comparator.name.value],
        backend_config=backend_config,
        result_shapes=result_shapes)
  else:
    # Older versions do not support has_side_effect attribute; we just use
    # the old lowering code.
    if any(not core.is_constant_shape(aval_out.shape) for aval_out in ctx.avals_out):
      raise ValueError("approx_top_k not supported with shape polymorphism; "
                       "try upgrading jaxlib")
    out = hlo.CustomCallOp([mlir.aval_to_ir_type(aval) for aval in ctx.avals_out],
                          [operand, iota, init_val, init_arg],
                          call_target_name=b"ApproxTopK",
                          called_computations=mlir.ir.ArrayAttr.get(
              [mlir.ir.FlatSymbolRefAttr.get(comparator.name.value)]))
    backend_config_attr = mlir.ir.DictAttr.get(backend_config,
                                              ctx.module_context.context)
    out.operation.attributes["mhlo.backend_config"] = backend_config_attr

  return out.results
