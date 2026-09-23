def finalize_out_shardings(out_shardings, are_out_shardings_from_xla,
                           device_assignment):
  if len(device_assignment) == 1:
    return ([SingleDeviceSharding(device_assignment[0], memory_kind=o.memory_kind)
             if isinstance(o, GSPMDSharding) else o for o in out_shardings],
            are_out_shardings_from_xla)
  return out_shardings, are_out_shardings_from_xla
