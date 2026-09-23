def run_state(f: Callable[..., None]):
  def wrapped(args):
    flat_args, in_tree = tree_util.tree_flatten(args)
    avals = [core.raise_to_shaped(core.get_aval(arg)) for arg in flat_args]
    jaxpr_, consts, _ = initial_style_jaxpr(f, in_tree, map(AbstractRef, avals))
    jaxpr = hoist_consts_to_refs(jaxpr_)
    which_linear = (False,) * (len(consts) + len(flat_args))
    out_const_flat = run_state_p.bind(*consts, *flat_args, jaxpr=jaxpr,
                                      which_linear=which_linear)
    _, out_flat = split_list(out_const_flat, [len(consts)])
    return in_tree.unflatten(out_flat)
  return wrapped
