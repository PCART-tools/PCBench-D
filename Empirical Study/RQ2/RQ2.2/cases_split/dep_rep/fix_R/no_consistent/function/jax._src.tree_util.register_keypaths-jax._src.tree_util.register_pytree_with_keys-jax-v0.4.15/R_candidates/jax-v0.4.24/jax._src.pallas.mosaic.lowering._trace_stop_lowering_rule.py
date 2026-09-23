def _trace_stop_lowering_rule(ctx: LoweringRuleContext):
  return tpu.TraceStopOp().results
