def emit_python_callback(
    ctx: LoweringRuleContext, callback, token: Optional[Any],
    operands: List[ir.Value], operand_avals: List[core.ShapedArray],
    result_avals: List[core.ShapedArray],
    has_side_effect: bool, *, sharding: Optional[xc.OpSharding] = None,
    operand_layouts: Optional[Sequence[Optional[Sequence[int]]]] = None,
    result_layouts: Optional[Sequence[Optional[Sequence[int]]]] = None,
    ) -> Tuple[List[ir.Value], Any, Any]:
  """Emits MLIR that calls back to a provided Python function."""
  platform = ctx.module_context.platform
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
    operand_layouts = map(_aval_to_default_layout, operand_avals)
  operand_mlir_layouts = [
      _layout_to_mlir_layout(_aval_to_default_layout(layout)) if layout is None
      else _layout_to_mlir_layout(layout) for layout, aval
      in zip(operand_layouts, operand_avals)]
  if result_layouts is None:
    result_layouts = map(_aval_to_default_layout, result_avals)
  result_mlir_layouts = [
      _layout_to_mlir_layout(_aval_to_default_layout(aval)) if layout is None
      else _layout_to_mlir_layout(layout) for layout, aval
      in zip(result_layouts, result_avals)]

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
    return out_vals

  if platform == "tpu":
    return _emit_tpu_python_callback(backend, ctx, _wrapped_callback,  token,
        operands, operand_avals, operand_shapes, result_avals, result_shapes,
        sharding=sharding)
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
  callback_descriptor, keepalive = (
      backend.get_emit_python_callback_descriptor(_wrapped_callback,
                                                  operand_shapes,
                                                  result_shapes))
  descriptor_operand = ir_constant(
      callback_descriptor, canonicalize_types=False)
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
      hlo.GetTupleElementOp(result, i32_attr(i)).result
      for i in range(len(result_types))
  ]
  if token:
    token, *results = results
  return results, token, keepalive
