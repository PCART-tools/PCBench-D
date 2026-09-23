def sharded_lowering(fun, name, donated_invars, keep_unused,
                     *arg_specs, lowering_platform: Optional[str]):
  in_avals, in_shardings = util.unzip2(arg_specs)
  in_shardings = [pxla._UNSPECIFIED if i is None else i for i in in_shardings]  # type: ignore

  # Pass in a singleton `_UNSPECIFIED` for out_shardings because we don't know
  # the number of output avals at this stage. lower_sharding_computation will
  # apply it to all out_avals.
  return pxla.lower_sharding_computation(
      fun, 'jit', name, in_shardings, pxla._UNSPECIFIED, donated_invars,
      in_avals, keep_unused=keep_unused, always_lower=False,
      devices_from_context=None, lowering_platform=lowering_platform)
