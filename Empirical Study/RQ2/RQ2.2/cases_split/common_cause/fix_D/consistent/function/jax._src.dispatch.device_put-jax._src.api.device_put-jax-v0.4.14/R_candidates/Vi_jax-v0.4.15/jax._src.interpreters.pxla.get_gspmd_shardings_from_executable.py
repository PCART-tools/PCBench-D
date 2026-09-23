def get_gspmd_shardings_from_executable(
    xla_executable, device_assignment: Sequence[xc.Device],
    num_out_avals: int
) -> Sequence[sharding_impls.XLACompatibleSharding]:
  from jax._src import pjit

  if config.jax_enable_memories:
    try:
      omk = xla_executable.get_output_memory_kinds()[0]
    except:
      omk = [None] * num_out_avals
  else:
    omk = [None] * num_out_avals

  # When the device assignment only has 1 device, SPMD partitioner will not run.
  # Hence the op shardings will not be set on the `hlo_module`. In that case,
  # just return SingleDeviceShardings since we know the computation is running
  # only on 1 device.
  if len(device_assignment) == 1:
    return [sharding_impls.SingleDeviceSharding(device_assignment[0], memory_kind=mk)
            for mk in omk]

  _, out_op_shardings = pjit.get_op_sharding_from_executable(xla_executable)

  # This condition happens when all the elements in the output tuple have the
  # same sharding, so XLA decides to run the `FusionTupleDeduplicator` to
  # put the sharding on ROOT instead of the tuple.
  # TODO(b/245667823): Remove this when XLA fixes this.
  if len(out_op_shardings) == 1 and len(out_op_shardings) < num_out_avals:
    out_op_shardings = out_op_shardings * num_out_avals  # type: ignore

  assert len(out_op_shardings) == num_out_avals == len(omk), (
      len(out_op_shardings), num_out_avals, len(omk))

  return [sharding_impls.GSPMDSharding(device_assignment, os, memory_kind=mk)
          for os, mk in safe_zip(out_op_shardings, omk)]
