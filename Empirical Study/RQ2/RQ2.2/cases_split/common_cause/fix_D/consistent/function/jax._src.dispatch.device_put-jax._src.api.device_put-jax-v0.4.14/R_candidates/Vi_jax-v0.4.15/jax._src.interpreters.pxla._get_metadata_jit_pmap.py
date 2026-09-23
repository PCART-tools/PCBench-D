def _get_metadata_jit_pmap(local_devices, num_in_shardings, num_out_shardings):
  # Create replicated shardings for jit(pmap) path with local devices
  # because multihost jit(pmap) is not allowed.
  gs = sharding_impls.GSPMDSharding.get_replicated(local_devices)
  in_shardings = [gs] * num_in_shardings
  out_shardings = [gs] * num_out_shardings
  # jit(pmap) will generate Arrays with multi-device sharding.
  # It is unsupported for these shardings to be uncommited, so force
  # the outputs to be committed.
  committed = True
  return in_shardings, out_shardings, committed, tuple(local_devices)
