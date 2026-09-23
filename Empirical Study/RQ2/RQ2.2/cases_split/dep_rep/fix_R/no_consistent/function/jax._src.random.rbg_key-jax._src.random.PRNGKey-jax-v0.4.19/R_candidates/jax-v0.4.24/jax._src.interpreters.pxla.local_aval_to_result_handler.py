def local_aval_to_result_handler(
    aval: core.AbstractValue,
    sharding: sharding_impls.XLACompatibleSharding,
    indices: tuple[Index, ...] | None,
) -> Callable[[list[xc.ArrayImpl]], Any]:
  """Returns a function for handling the raw buffers of a single output aval.

  Args:
    aval: The local output AbstractValue.
    sharding_spec: Indicates how the output is sharded across devices, or None
      for non-array avals.
    indices: The pre-computed result of spec_to_indices, or None for non-array
      avals.

  Returns:
    A function for handling the Buffers that will eventually be produced
    for this output. The function will return an object suitable for returning
    to the user, e.g. an Array.
  """
  try:
    return local_result_handlers[(type(aval))](aval, sharding, indices)
  except KeyError as err:
    raise TypeError(
        f"No pxla_result_handler for type: {type(aval)}") from err
