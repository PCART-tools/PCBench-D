def sharded_lowering(
    fun: lu.WrappedFun, name: str, donated_invars: Sequence[bool],
    keep_unused: bool, inline: bool, in_avals: tuple[core.AbstractValue, ...],
    in_shardings: Sequence[Sharding | None], lowering_platform: str | None
) -> pxla.MeshComputation:
  in_shardings_unspec = [UNSPECIFIED if i is None else i for i in in_shardings]

  # Pass in a singleton `UNSPECIFIED` for out_shardings because we don't know
  # the number of output avals at this stage. lower_sharding_computation will
  # apply it to all out_avals.
  return pxla.lower_sharding_computation(
      fun, 'jit', name, in_shardings_unspec, UNSPECIFIED, donated_invars,
      in_avals, keep_unused=keep_unused, inline=inline, always_lower=False,
      devices_from_context=None, lowering_platform=lowering_platform)
