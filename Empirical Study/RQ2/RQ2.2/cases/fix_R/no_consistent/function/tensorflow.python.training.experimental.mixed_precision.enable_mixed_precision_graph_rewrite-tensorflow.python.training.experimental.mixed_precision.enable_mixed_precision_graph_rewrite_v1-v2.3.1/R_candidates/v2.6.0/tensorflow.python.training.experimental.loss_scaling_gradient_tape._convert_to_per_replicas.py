def _convert_to_per_replicas(distribution, values):
  """Converts tensors and DistributedVariables to PerReplica values.

  Args:
    distribution: The distribution strategy in effect.
    values: A list of tensors, variables, DistributedValues, or anything else
      that can be converted to a PerReplcia value

  Returns:
    `values`, but each element has been converted to a PerReplica value.
  """
  return distribution.run(
      lambda values: [array_ops.identity(v) for v in values],
      args=(values,)
  )
