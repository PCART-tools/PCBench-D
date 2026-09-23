def sharded_lowering(fun, name, donated_invars, keep_unused, inline,
                     in_avals, in_shardings, lowering_platform: str | None):
  if isinstance(in_shardings, OrigShardings):
    in_shardings = in_shardings.shardings

  in_shardings = [UNSPECIFIED if i is None else i for i in in_shardings]  # type: ignore

  # Pass in a singleton `UNSPECIFIED` for out_shardings because we don't know
  # the number of output avals at this stage. lower_sharding_computation will
  # apply it to all out_avals.
  return pxla.lower_sharding_computation(
      fun, 'jit', name, in_shardings, UNSPECIFIED, donated_invars,
      tuple(in_avals), keep_unused=keep_unused, inline=inline, always_lower=False,
      devices_from_context=None, lowering_platform=lowering_platform)
