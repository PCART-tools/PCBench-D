def cond_error_check(error, enabled_errors, index, *ops, branches, linear):
  new_branches, msgs_ = unzip2(checkify_jaxpr(jxpr, error, enabled_errors)
                               for jxpr in branches)
  new_linear = (False, False, False, *linear)
  err, code, payload, *outs = lax.cond_p.bind(
      index, error.err, error.code, error.payload, *ops,
      branches=tuple(new_branches), linear=new_linear)
  new_msgs = {k:v for d in it.chain([error.msgs], msgs_) for k, v in d.items()}
  return outs, Error(err, code, new_msgs, payload)
