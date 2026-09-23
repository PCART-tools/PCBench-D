  @traceback_util.api_boundary
  def __call__(self, *args: Any, **kwargs: Any) -> ReturnValue:  # pytype: disable=invalid-annotation
    primal_name = getattr(self.fun, '__name__', str(self.fun))
    if not self.jvp:
      msg = f"No JVP defined for custom_jvp function {primal_name} using defjvp."
      raise AttributeError(msg)
    jvp_name    = getattr(self.jvp, '__name__', str(self.jvp))
    args = _resolve_kwargs(self.fun, args, kwargs)
    if self.nondiff_argnums:
      nondiff_argnums = set(self.nondiff_argnums)
      args = tuple(_stop_gradient(x) if i in nondiff_argnums else x
                   for i, x in enumerate(args))
      diff_argnums = [i for i in range(len(args)) if i not in nondiff_argnums]
      f_, dyn_args = argnums_partial(lu.wrap_init(self.fun), diff_argnums, args,
                                     require_static_args_hashable=False)
      static_args = [args[i] for i in self.nondiff_argnums]
      jvp = _add_args(lu.wrap_init(self.jvp), static_args)
    else:
      f_, dyn_args = lu.wrap_init(self.fun), args  # type: ignore
      jvp = lu.wrap_init(self.jvp)
    args_flat, in_tree = tree_flatten(dyn_args)
    flat_fun, out_type1 = _flatten_fun_nokwargs(f_, in_tree)
    flat_jvp, out_type2 = _flatten_jvp(jvp, primal_name, jvp_name, in_tree,
                                       out_type1)
    out_flat = custom_jvp_call_p.bind(flat_fun, flat_jvp, *args_flat,
                                      symbolic_zeros=self.symbolic_zeros)
    _, (out_tree, _) = lu.merge_linear_aux(out_type1, out_type2)
    return tree_unflatten(out_tree, out_flat)
