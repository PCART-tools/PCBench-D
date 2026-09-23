def _semaphore_wait_lowering_rule(ctx: LoweringRuleContext, *args, args_tree):
  sem_aval, _, _ = tree_util.tree_unflatten(args_tree, ctx.avals_in)
  sem, indexers, value = tree_util.tree_unflatten(args_tree, args)
  sem, _, _ = _index_ref(sem, sem_aval, sem_aval.shape, indexers)
  return tpu.SemaphoreWaitOp(sem, value).results
