def _inner_partitions(jaxpr, expected_num_parts: Optional[int]):
  """Returns the total number of partitions from PartitionSpecs inside `jaxpr`.

  Also validates that this number matches `expected_num_parts` if provided.
  """
  for eqn in jaxpr.eqns:
    if eqn.primitive.name in ["sharding_constraint", "infeed"]:
      parts = eqn.params["partitions"]
      nparts = get_num_partitions(parts)
      if expected_num_parts is None:
        expected_num_parts = nparts
      elif nparts is not None and nparts != expected_num_parts:
        # TODO(skye): raise this error as we trace the jaxpr
        raise ValueError(
            f"with_sharding_constraint with partitions={parts} "
            f"(total partitions: {nparts}) doesn't match expected number of "
            f"partitions: {expected_num_parts}. If these partitions look "
            f"right, check outer sharded_jit and/or other "
            f"with_sharding_constraint calls.")
    else:
      for subjaxpr in core.jaxprs_in_params(eqn.params):
        expected_num_parts = _inner_partitions(subjaxpr, expected_num_parts)
  return expected_num_parts
