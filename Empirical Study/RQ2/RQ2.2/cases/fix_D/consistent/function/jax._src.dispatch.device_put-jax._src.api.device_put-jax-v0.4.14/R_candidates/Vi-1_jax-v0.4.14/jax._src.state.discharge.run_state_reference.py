def run_state_reference(f: Callable[..., None]):
  def wrapped(args):
    flat_args, in_tree = tree_util.tree_flatten(args)
    avals = [core.raise_to_shaped(core.get_aval(arg)) for arg in flat_args]
    jaxpr_, consts, _ = initial_style_jaxpr(f, in_tree, map(AbstractRef, avals))
    jaxpr = hoist_consts_to_refs(jaxpr_)
    discharged_jaxpr, discharged_consts = discharge_state(jaxpr, ())
    out_const_flat = core.eval_jaxpr(discharged_jaxpr, discharged_consts,
                                     *consts, *args)
    _, out_flat = split_list(out_const_flat, [len(consts)])
    return in_tree.unflatten(out_flat)
  return wrapped
