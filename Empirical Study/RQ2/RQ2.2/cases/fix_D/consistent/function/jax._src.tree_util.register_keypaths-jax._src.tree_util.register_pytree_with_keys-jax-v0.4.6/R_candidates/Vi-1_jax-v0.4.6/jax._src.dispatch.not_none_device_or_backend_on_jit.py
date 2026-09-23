def not_none_device_or_backend_on_jit(backend, device, num_ins):
  """This is to support the backend and device argument on jit. It's a feature
  that's deprecated but needs to be supported for feature parity and so that we
  can delete the non-Array paths when Array is switched on.
  """
  # TODO(yashkatariya): Remove this entire function when backend and device are
  # removed as arguments on jit.
  if device is not None and backend is not None:
    raise ValueError("can't specify both a device and a backend for jit, "
                     "got device={} and backend={}".format(device, backend))

  if backend is not None:
    da = [xb.get_backend(backend).get_default_device_assignment(1)[0]]
  else:
    assert device is not None
    da = [device]

  assert len(da) == 1
  # in_shardings will be marked as replicated regardless of whatever the input
  # had. Given that only a single device is allowed above, this is correct.
  in_shardings = [GSPMDSharding.get_replicated(da)] * num_ins
  return da, in_shardings
