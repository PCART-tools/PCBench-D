@weakref_lru_cache
def _partial_eval_jaxpr_nounits(jaxpr, in_unknowns, instantiate):
  f = lu.wrap_init(core.jaxpr_as_fun(jaxpr))

  cell = []
  def fun(*known_vals_in):
    known_vals_in = iter(known_vals_in)
    unknown_avals = (a for a, uk in zip(jaxpr.in_avals, in_unknowns) if uk)
    in_pvals = [PartialVal.unknown(next(unknown_avals)) if uk
                else PartialVal.known(next(known_vals_in)) for uk in in_unknowns]
    assert next(known_vals_in, None) is next(unknown_avals, None) is None
    jaxpr_unknown_, out_pvals, residuals = trace_to_jaxpr_nounits(
        f, in_pvals, instantiate=instantiate)
    jaxpr_unknown = convert_constvars_jaxpr(jaxpr_unknown_)
    out_unknowns = [not pval.is_known() for pval in out_pvals]
    res_avals = [core.raise_to_shaped(core.get_aval(r)) for r in residuals]
    cell.append((out_unknowns, jaxpr_unknown, res_avals))
    known_vals_out = [pval.get_known() for pval in out_pvals if pval.is_known()]
    return [*known_vals_out, *residuals]

  known_avals = [a for a, uk in zip(jaxpr.in_avals, in_unknowns) if not uk]
  jaxpr_known, _, consts_known, () = trace_to_jaxpr_dynamic(lu.wrap_init(fun), known_avals)
  (out_unknowns, jaxpr_unknown, res_avals), = cell  # pytype: disable=bad-unpacking

  # check jaxpr_known and jaxpr_unknown in isolation
  # TODO(mattjj): enable weak type checking here
  if config.enable_checks.value:
    core.check_jaxpr(jaxpr_known)
    core.check_jaxpr(jaxpr_unknown)
  # check jaxpr_known has input type corresponding to known inputs of jaxpr
  assert ([v.aval for v in jaxpr_known.invars] ==
          [a for a, uk in zip(jaxpr.in_avals, in_unknowns) if not uk])
  # check jaxpr_known has out type corresponding to known outs of jaxpr plus res
  assert ([v.aval.strip_weak_type() for v in jaxpr_known.outvars] ==
          [a.strip_weak_type() for a, uk in zip(jaxpr.out_avals, out_unknowns)
           if not uk] + [a.strip_weak_type() for a in res_avals])
  # check jaxpr_unknown has input type corresponding to res plus unknown inputs
  assert ([v.aval.strip_weak_type() for v in jaxpr_unknown.invars] ==
          [a.strip_weak_type() for a in res_avals] +
          [a.strip_weak_type() for a, uk in zip(jaxpr.in_avals, in_unknowns)
           if uk])
  # check jaxpr_unknown has output type corresponding to unknown outputs
  assert ([v.aval.strip_weak_type() for v in jaxpr_unknown.outvars] ==
          [a.strip_weak_type() for a, uk in zip(jaxpr.out_avals, out_unknowns)
           if uk])

  closed_jaxpr_known = ClosedJaxpr(jaxpr_known, consts_known)
  closed_jaxpr_unknown = ClosedJaxpr(jaxpr_unknown, ())
  return closed_jaxpr_known, closed_jaxpr_unknown, out_unknowns, res_avals
