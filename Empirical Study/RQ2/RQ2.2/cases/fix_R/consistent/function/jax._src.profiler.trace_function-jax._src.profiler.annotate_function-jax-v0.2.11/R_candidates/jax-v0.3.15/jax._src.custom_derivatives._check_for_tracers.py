def _check_for_tracers(x):
  for leaf in tree_leaves(x):
    if isinstance(x, core.Tracer):
      msg = ("Found a JAX Tracer object passed as an argument to a custom_vjp "
            "function in a position indicated by nondiff_argnums as "
            "non-differentiable. Tracers cannot be passed as non-differentiable "
            "arguments to custom_vjp functions; instead, nondiff_argnums should "
            "only be used for arguments that can't be or contain JAX tracers, "
            "e.g. function-valued arguments. In particular, array-valued "
            "arguments should typically not be indicated as nondiff_argnums.")
      raise UnexpectedTracerError(msg)
