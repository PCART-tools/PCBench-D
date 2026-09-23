@weakref_lru_cache
def _trace_to_jaxpr(fun, in_tree, in_avals):
  flat_fun, out_tree = flatten_fun(lu.wrap_init(fun), in_tree)
  debug = pe.debug_info(fun, in_tree, out_tree, True, "checkpoint")
  try:
    jaxpr, _, consts = pe.trace_to_jaxpr_dynamic(flat_fun, in_avals, debug)
  except core.ConcretizationTypeError as e:
    msg, = e.args
    if 'for checkpoint' not in msg:
      raise
    new_msg = msg + "\n\n" + (
        "Consider using the `static_argnums` parameter for `jax.remat` or "
        "`jax.checkpoint`. See the `jax.checkpoint` docstring and its example "
        "involving `static_argnums`:\n"
        "https://jax.readthedocs.io/en/latest/_autosummary/jax.checkpoint.html"
        "\n")
    new_e = core.ConcretizationTypeError.__new__(core.ConcretizationTypeError)
    new_e.args = (new_msg,)
    raise new_e from None
  return pe.convert_constvars_jaxpr(jaxpr), consts, out_tree()
