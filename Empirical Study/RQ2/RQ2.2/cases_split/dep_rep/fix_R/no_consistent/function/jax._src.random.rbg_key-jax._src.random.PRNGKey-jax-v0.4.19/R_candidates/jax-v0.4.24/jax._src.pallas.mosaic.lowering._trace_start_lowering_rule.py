def _trace_start_lowering_rule(
    ctx: LoweringRuleContext, *, message: str, level: int
):
  return tpu.TraceStartOp(message=message, level=level).results
