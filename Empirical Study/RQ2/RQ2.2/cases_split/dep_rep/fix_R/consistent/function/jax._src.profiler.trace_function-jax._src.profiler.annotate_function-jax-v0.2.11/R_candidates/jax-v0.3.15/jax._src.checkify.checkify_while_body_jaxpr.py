def checkify_while_body_jaxpr(cond_jaxpr, body_jaxpr, error, enabled_errors, c_consts):
  cond_f = core.jaxpr_as_fun(cond_jaxpr)
  body_f = core.jaxpr_as_fun(body_jaxpr)
  def new_body_f(*vals):
    out = body_f(*vals)
    # This checks if the next cond application will error
    _ = cond_f(*c_consts, *out)
    return out
  return checkify_fun_to_jaxpr(lu.wrap_init(new_body_f), error, enabled_errors,
                               body_jaxpr.in_avals)
