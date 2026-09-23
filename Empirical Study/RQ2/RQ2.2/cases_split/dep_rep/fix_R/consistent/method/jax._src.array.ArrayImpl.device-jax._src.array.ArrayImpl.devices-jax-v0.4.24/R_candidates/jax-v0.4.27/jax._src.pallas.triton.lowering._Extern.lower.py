  def lower(self, ctx: LoweringRuleContext, *args: Sequence[ir.Value]):
    [out_aval] = ctx.avals_out
    result_type = _dtype_to_ir_type(jnp.dtype(self.result_type))
    if out_aval.shape:
      result_type = ir.RankedTensorType.get(out_aval.shape, result_type)
    return tt_dialect.extern_elementwise(
        result_type,
        args,
        libname="",
        libpath="",
        symbol=self.symbol,
        pure=True,
    )
