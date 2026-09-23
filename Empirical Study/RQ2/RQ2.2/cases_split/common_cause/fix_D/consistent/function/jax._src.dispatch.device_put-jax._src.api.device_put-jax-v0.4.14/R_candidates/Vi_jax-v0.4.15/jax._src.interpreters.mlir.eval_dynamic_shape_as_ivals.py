def eval_dynamic_shape_as_ivals(
    ctx: LoweringRuleContext, shape: core.Shape
    ) -> tuple[int | Value, ...]:
  """Evaluates the dynamic shapes as int or ir.int32 values."""
  def convert_dim(d: int | Value) -> int | ir.Value:
    if type(d) is int:
      return d
    else:
      i32_type = aval_to_ir_type(core.ShapedArray((), np.int32))
      if d.type != i32_type:  # type: ignore
        return hlo.ConvertOp(i32_type, d).result
      else:
        return d
  return tuple(convert_dim(v) for v in eval_dynamic_shape(ctx, shape))
