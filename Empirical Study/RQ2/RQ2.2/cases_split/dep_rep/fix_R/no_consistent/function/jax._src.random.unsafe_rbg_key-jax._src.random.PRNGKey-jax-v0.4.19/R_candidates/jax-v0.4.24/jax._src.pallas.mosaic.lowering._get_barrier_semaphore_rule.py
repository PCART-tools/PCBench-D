def _get_barrier_semaphore_rule(ctx: LoweringRuleContext):
  memref_type = aval_to_ir_type(ctx.avals_out[0])
  return tpu.GetBarrierSemaphoreOp(memref_type).result
