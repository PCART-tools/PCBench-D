def global_aval_to_result_handler(
    aval: core.AbstractValue, out_sharding, committed: bool,
    is_out_sharding_from_xla: bool
) -> Callable[[Sequence[xb.xla_client.Buffer]], Any]:
  """Returns a function for handling the raw buffers of a single output aval.

  Args:
    aval: The global output AbstractValue.
    out_axis_resources: A PartitionSpec specifying the sharding of outputs.
      Used for creating GSDAs.
    global_mesh: The global device mesh that generated this output. Used
      for creating GSDAs.
    is_out_sharding_from_xla: True, if the out_sharding comes from XLA i.e.
      the sharding is extracted from the HLO.

  Returns:
    A function for handling the Buffers that will eventually be produced
    for this output. The function will return an object suitable for returning
    to the user, e.g. a ShardedDeviceArray.
  """
  if config.jax_array:
    output_type = OutputType.Array
  elif config.jax_parallel_functions_output_gda:
    output_type = OutputType.GlobalDeviceArray
  try:
    return global_result_handlers[(type(aval), output_type)](
        aval, out_sharding, committed, is_out_sharding_from_xla)
  except KeyError as err:
    raise TypeError(
        f"No pxla_result_handler for type: {type(aval)}") from err
