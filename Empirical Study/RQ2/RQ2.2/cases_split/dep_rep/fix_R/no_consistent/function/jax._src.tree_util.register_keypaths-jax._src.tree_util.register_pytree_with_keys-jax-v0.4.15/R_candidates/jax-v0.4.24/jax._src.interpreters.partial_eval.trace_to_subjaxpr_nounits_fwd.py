@lu.transformation
def trace_to_subjaxpr_nounits_fwd(
    main: core.MainTrace,
    instantiate: bool | Sequence[bool],
    in_pvals: Sequence[PartialVal]):
  assert all(isinstance(pv, PartialVal) for pv in in_pvals), in_pvals
  out_tracers, jaxpr, out_consts, env = yield from _trace_to_subjaxpr_nounits(
      main, instantiate, in_pvals)
  out_pvals = [t.pval for t in out_tracers]

  # Which out_consts (aka residuals) are just forwarded inputs? Check obj id.
  in_consts  = [pval.get_known()    for pval in in_pvals if     pval.is_known()]
  id_map = {id(c): i for i, c in enumerate(in_consts)}
  fwds: list[int | None] = [id_map.get(id(c)) for c in out_consts]
  pruned_consts = [c for c, fwd in zip(out_consts, fwds) if fwd is None]

  del out_tracers
  yield jaxpr, (fwds, out_pvals, pruned_consts, env)
