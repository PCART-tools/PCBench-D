def eval_dynamic_shape_as_vals(ctx: LoweringRuleContext,
                               shape: core.Shape) -> tuple[Value, ...]:
  """Evaluates the dynamic shapes as int32 values."""
  def convert_dim(d: int | Value):
    if type(d) is int:
      return ir_constant(np.array(d, dtype=np.int32))
    else:
      i32_type = aval_to_ir_type(core.ShapedArray((), np.int32))
      if d.type != i32_type:  # type: ignore
        return hlo.convert(i32_type, d)
      else:
        return d
  return tuple(convert_dim(v) for v in eval_dynamic_shape(ctx, shape))
