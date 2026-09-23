@profiler.annotate_function
def shard_args(
    shardings: Sequence[sharding_impls.XLACompatibleSharding], args,
) -> Sequence[jax.Array]:
  return [shard_arg(arg, shardings[i]) for i, arg in enumerate(args)]
