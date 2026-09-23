def _lift_linearized(jaxpr, primal_avals, io_tree, out_pvals, consts, *py_args):
  def fun(*tangents):
    tangent_avals = list(map(core.get_aval, tangents))
    for primal_aval, tangent_aval in zip(primal_avals, tangent_avals):
      if not core.typecompat(primal_aval.at_least_vspace(), tangent_aval):
        raise ValueError("linearized function called on tangent values inconsistent with "
                         "the original primal values: "
                         f"got {tangent_aval} for primal aval {primal_aval}")
    tangents_out = eval_jaxpr(jaxpr, consts, *tangents)
    tangents_out_ = iter(tangents_out)
    full_out = [pval.get_known() if pval.is_known() else next(tangents_out_)
                for pval in out_pvals]
    assert next(tangents_out_, None) is None
    return full_out

  return apply_flat_fun_nokwargs(fun, io_tree, py_args)
