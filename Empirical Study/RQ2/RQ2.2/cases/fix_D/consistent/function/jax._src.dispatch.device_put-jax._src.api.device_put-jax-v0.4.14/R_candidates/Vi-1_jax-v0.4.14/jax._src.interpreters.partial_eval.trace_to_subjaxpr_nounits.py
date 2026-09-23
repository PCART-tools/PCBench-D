@lu.transformation
def trace_to_subjaxpr_nounits(
    main: core.MainTrace,
    instantiate: bool | Sequence[bool],
    in_pvals: Sequence[PartialVal]):
  assert all([isinstance(pv, PartialVal) for pv in in_pvals]), in_pvals
  out_tracers, jaxpr, out_consts, env = yield from _trace_to_subjaxpr_nounits(
      main, instantiate, in_pvals)
  out_pvals = [t.pval for t in out_tracers]
  del out_tracers
  yield jaxpr, (out_pvals, out_consts, env)
