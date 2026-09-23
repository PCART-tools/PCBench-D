def _execute_trivial(jaxpr, device: Optional[Device], consts, avals, handlers,
                     has_unordered_effects: bool,
                     ordered_effects: List[core.Effect], kept_var_idx,
                     host_callbacks, *args):
  env: Dict[core.Var, Any]  = {}
  pruned_args = (x for i, x in enumerate(args) if i in kept_var_idx)
  map(env.setdefault, jaxpr.invars, pruned_args)
  map(env.setdefault, jaxpr.constvars, consts)
  outs = [xla.canonicalize_dtype(v.val) if type(v) is core.Literal else env[v]
          for v in jaxpr.outvars]
  return [_copy_device_array_to_device(x, device) if device_array.type_is_device_array(x)
          else h(None, *device_put(x, device)) for h, x in zip(handlers, outs)]
