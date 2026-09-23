def get_gspmd_shardings_from_executable(
    xla_executable, device_assignment: Sequence[xc.Device],
    num_in_avals: int, num_out_avals: int
) -> Tuple[Sequence[sharding_impls.XLACompatibleSharding],
           Sequence[sharding_impls.XLACompatibleSharding]]:
  from jax.experimental import pjit

  # When the device assignment only has 1 device, SPMD partitioner will not run.
  # Hence the op shardings will not be set on the `hlo_module`. In that case,
  # just return SingleDeviceShardings since we know the computation is running
  # only on 1 device.
  if len(device_assignment) == 1:
    return ([sharding_impls.SingleDeviceSharding(device_assignment[0])
             for _ in range(num_in_avals)],
            [sharding_impls.SingleDeviceSharding(device_assignment[0])
             for _ in range(num_out_avals)])

  in_op_shardings, out_op_shardings = pjit._get_op_sharding_from_executable(xla_executable)

  in_shardings_xla = [sharding_impls.GSPMDSharding(device_assignment, i)
                      for i in in_op_shardings]
  out_shardings_xla = [sharding_impls.GSPMDSharding(device_assignment, o)
                       for o in out_op_shardings]
  # This condition happens when all the elements in the output tuple have the
  # same sharding, so XLA decides to run the `FusionTupleDeduplicator` to
  # put the sharding on ROOT instead of the tuple.
  # TODO(b/245667823): Remove this when XLA fixes this.
  if len(out_shardings_xla) == 1 and len(out_shardings_xla) < num_out_avals:
    out_shardings_xla = out_shardings_xla * num_out_avals
  assert len(out_shardings_xla) == num_out_avals, (
      len(out_shardings_xla), num_out_avals)
  return in_shardings_xla, out_shardings_xla
