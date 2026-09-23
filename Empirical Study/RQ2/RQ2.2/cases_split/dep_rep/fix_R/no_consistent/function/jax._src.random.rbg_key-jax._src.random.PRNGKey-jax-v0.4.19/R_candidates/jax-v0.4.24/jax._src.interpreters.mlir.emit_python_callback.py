def emit_python_callback(
    ctx: LoweringRuleContext, callback, token: Any | None,
    operands: Sequence[ir.Value], operand_avals: Sequence[core.ShapedArray],
    result_avals: Sequence[core.ShapedArray],
    has_side_effect: bool, *, sharding: xc.OpSharding | None = None,
    operand_layouts: Sequence[Sequence[int] | None] | None = None,
    result_layouts: Sequence[Sequence[int] | None] | None = None,
    ) -> tuple[Sequence[ir.Value], Any, Any]:
  """Emits MLIR that calls back to a provided Python function."""
  if len(ctx.module_context.platforms) > 1:
    raise NotImplementedError("multi-platform lowering for python_callback")
  platform = ctx.module_context.platforms[0]
  if platform not in {"cpu", "cuda", "rocm", "tpu"}:
    raise ValueError(
        f"`EmitPythonCallback` not supported on {platform} backend.")
  backend = ctx.module_context.backend
  result_shapes = util.flatten(
      [xla.aval_to_xla_shapes(result_aval) for result_aval in result_avals])
  operand_shapes = util.flatten(
      [xla.aval_to_xla_shapes(op_aval) for op_aval in operand_avals])
  # Handling layouts
  if operand_layouts is None:
    operand_layouts = util.concatenate(
        map(_aval_to_default_layouts, operand_avals))
  operand_mlir_layouts = map(_layout_to_mlir_layout, operand_layouts)
  if result_layouts is None:
    result_layouts = util.concatenate(map(_aval_to_default_layouts, result_avals))
  result_mlir_layouts = map(_layout_to_mlir_layout, result_layouts)

  # First we apply checks to ensure output shapes and dtypes match the expected
  # ones.
  def _wrapped_callback(*args):
    out_vals = callback(*args)
    if len(out_vals) != len(result_avals):
      raise RuntimeError(
          "Mismatched number of outputs from callback. "
          "Expected: {}, Actual: {}".format(len(result_avals), len(out_vals)))
    for i, (out_val, out_aval) in enumerate(zip(out_vals, result_avals)):
      if out_val.shape != out_aval.shape:
        raise RuntimeError(
            f"Incorrect output shape for return value {i}: "
            "Expected: {}, Actual: {}".format(out_aval.shape, out_val.shape))
      if out_val.dtype != out_aval.dtype:
        raise RuntimeError(
            f"Incorrect output dtype for return value {i}: "
            "Expected: {}, Actual: {}".format(out_aval.dtype, out_val.dtype))
    if platform == "tpu":
      # On TPU we cannot receive empty arrays. So, we return from the wrapped
      # callback only the non-empty results, and we will create empty constants
      # in the receiving computation.
      # TODO(b/238239458): fix TPU Recv to work with empty arrays.
      non_empty_out_vals = tuple(
          out_val
          for out_val, result_aval in zip(out_vals, result_avals)
          if not is_empty_shape(result_aval.shape))
      return non_empty_out_vals
    else:
      return out_vals

  if platform == "tpu":
    non_empty_result_avals, non_empty_result_shapes = util.unzip2([
        (aval, shape)
        for aval, shape in zip(result_avals, result_shapes)
        if not is_empty_shape(aval.shape)])
    non_empty_outputs, token = _emit_tpu_python_callback(
        backend, ctx, _wrapped_callback,  token,
        operands, operand_avals, operand_shapes,
        non_empty_result_avals, non_empty_result_shapes,
        sharding=sharding)
    non_empty_outputs_iter = iter(non_empty_outputs)
    outputs = [
        ir_constant(np.zeros(result_aval.shape, dtype=result_aval.dtype))
        if is_empty_shape(result_aval.shape) else next(non_empty_outputs_iter)
        for result_aval in result_avals]
    return outputs, token, None

  result_types = util.flatten([aval_to_ir_types(aval) for aval in result_avals])
  if token:

    callback_without_token = _wrapped_callback
    def _wrapped_callback(token, *args):  # type: ignore  # pylint: disable=function-redefined
      return (token, *callback_without_token(*args))

    operand_shapes = [
        xla.aval_to_xla_shapes(core.abstract_token)[0], *operand_shapes
    ]
    result_shapes = [
        xla.aval_to_xla_shapes(core.abstract_token)[0], *result_shapes
    ]
    operands = [token, *operands]
    result_types = [token_type()[0], *result_types]
    operand_mlir_layouts = [_layout_to_mlir_layout(None), *operand_mlir_layouts]
    result_mlir_layouts = [_layout_to_mlir_layout(None), *result_mlir_layouts]
  callback_descriptor, ifrt_callback = (
      backend.get_emit_python_callback_descriptor(_wrapped_callback,
                                                  operand_shapes,
                                                  result_shapes))
  ctx.module_context.add_host_callback(ifrt_callback)
  descriptor_operand = ir_constant(callback_descriptor)
  callback_operands = [descriptor_operand, *operands]
  if operand_mlir_layouts is not None:
    operand_mlir_layouts = [_layout_to_mlir_layout([]), *operand_mlir_layouts]
  result_type = ir.TupleType.get_tuple(result_types)
  call_target_name = ("xla_python_gpu_callback"
                     if platform in {"cuda", "rocm"} else "xla_python_cpu_callback")
  result = hlo.CustomCallOp(
      [result_type],
      callback_operands,
      call_target_name=ir.StringAttr.get(call_target_name),
      has_side_effect=ir.BoolAttr.get(has_side_effect),
      api_version=i32_attr(2),
      called_computations=ir.ArrayAttr.get([]),
      backend_config=ir.StringAttr.get(str(callback_descriptor)),
      operand_layouts=(
        None if operand_mlir_layouts is None
        else ir.ArrayAttr.get(operand_mlir_layouts)),
      result_layouts=(
        None if result_mlir_layouts is None
        else ir.ArrayAttr.get(result_mlir_layouts)))
  if sharding is not None:
    set_sharding(result, sharding)
  results = [
      hlo.get_tuple_element(result, i32_attr(i))
      for i in range(len(result_types))
  ]
  if token:
    token, *results = results
  return results, token, ifrt_callback
