def _execute_trivial(jaxpr, consts, in_handler, out_handler, kept_var_idx, *args):
  env: Dict[core.Var, Any]  = {}
  pruned_args = (x for i, x in enumerate(args) if i in kept_var_idx)
  map(env.setdefault, jaxpr.invars, pruned_args)
  map(env.setdefault, jaxpr.constvars, consts)
  outs = [xla.canonicalize_dtype(v.val) if type(v) is core.Literal else env[v]
          for v in jaxpr.outvars]
  return out_handler(in_handler(outs))
