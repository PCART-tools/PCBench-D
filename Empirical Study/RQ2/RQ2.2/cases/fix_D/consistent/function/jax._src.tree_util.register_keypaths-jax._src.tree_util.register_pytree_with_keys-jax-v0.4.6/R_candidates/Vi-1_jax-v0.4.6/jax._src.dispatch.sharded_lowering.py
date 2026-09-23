def sharded_lowering(fun, device, backend, name, donated_invars, always_lower,
                     keep_unused, *arg_specs,
                     lowering_platform: Optional[str]):
  in_avals, in_shardings = util.unzip2(arg_specs)

  da = None
  if backend is not None or device is not None:
    da, in_shardings = not_none_device_or_backend_on_jit(
        backend, device, len(in_shardings))

  in_shardings = [pxla._UNSPECIFIED if i is None else i for i in in_shardings]  # type: ignore

  # Pass in a singleton `_UNSPECIFIED` for out_shardings because we don't know
  # the number of output avals at this stage. lower_sharding_computation will
  # apply it to all out_avals.
  return pxla.lower_sharding_computation(
      fun, 'jit', name, in_shardings, pxla._UNSPECIFIED, donated_invars,
      in_avals, in_is_global=(True,) * len(arg_specs), keep_unused=keep_unused,
      always_lower=always_lower, devices_from_context=da,
      lowering_platform=lowering_platform)
