@cache()
def _variadic_reduction_jaxpr(computation, flat_avals, aval_tree):
  avals = tree_util.tree_unflatten(aval_tree, flat_avals)
  flat_in_avals, in_tree = tree_util.tree_flatten((avals, avals))
  comp = lu.wrap_init(computation)
  flat_comp, out_tree = api_util.flatten_fun_nokwargs(comp, in_tree)
  jaxpr, _, consts = pe.trace_to_jaxpr_dynamic(flat_comp, tuple(flat_in_avals))
  if any(isinstance(c, core.Tracer) for c in consts):
    raise NotImplementedError(
        "Reduction computations can't close over Tracers. Please open an issue "
        "at https://github.com/google/jax.")
  return jaxpr, tuple(consts), out_tree()
