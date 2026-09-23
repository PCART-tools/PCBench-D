def checkify_while_body_jaxpr(
    cond_jaxpr: core.ClosedJaxpr, body_jaxpr: core.ClosedJaxpr,
    enabled_errors, error: Error,
    c_consts) -> Tuple[core.ClosedJaxpr, PyTreeDef, Set[ErrorEffect]]:
  cond_f = core.jaxpr_as_fun(cond_jaxpr)
  body_f = core.jaxpr_as_fun(body_jaxpr)
  def new_body_f(*vals):
    out = body_f(*vals)
    # This checks if the next cond application will error
    _ = cond_f(*c_consts, *out)
    return out
  new_body_f_ = lu.wrap_init(new_body_f)
  jaxpr, _, consts = pe.trace_to_jaxpr_dynamic(new_body_f_, body_jaxpr.in_avals)
  closed_jaxpr = core.ClosedJaxpr(jaxpr, consts)
  err_vals, err_tree = jtu.tree_flatten(error)
  err_vals = map(get_shaped_aval, err_vals)
  flat_err_and_in_vals = [*err_vals, *body_jaxpr.in_avals]
  jaxpr, out_tree, error_effects = jaxpr_to_checkify_jaxpr(
      closed_jaxpr, enabled_errors, err_tree, *flat_err_and_in_vals)
  return jaxpr, out_tree, error_effects
