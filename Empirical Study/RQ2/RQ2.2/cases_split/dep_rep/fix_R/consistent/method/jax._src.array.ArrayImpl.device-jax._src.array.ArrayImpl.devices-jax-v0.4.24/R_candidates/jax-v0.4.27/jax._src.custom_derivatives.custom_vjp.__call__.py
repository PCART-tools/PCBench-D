  @traceback_util.api_boundary
  def __call__(self, *args: Any, **kwargs: Any) -> ReturnValue:  # pytype: disable=invalid-annotation
    primal_name = getattr(self.fun, '__name__', str(self.fun))
    if not self.fwd or not self.bwd:
      msg = f"No VJP defined for custom_vjp function {primal_name} using defvjp."
      raise AttributeError(msg)
    fwd_name = getattr(self.fwd, '__name__', str(self.fwd))
    args = _resolve_kwargs(self.fun, args, kwargs)
    if config.enable_custom_vjp_by_custom_transpose.value:
      if self.nondiff_argnums:
        raise NotImplementedError(
            'nondiff_argnums not implemented for new custom_vjp')
      return custom_vjp_by_custom_transpose(self.fun, self.fwd, self.bwd)(*args)
    else:
      if self.nondiff_argnums:
        for i in self.nondiff_argnums: _check_for_tracers(args[i])
        nondiff_argnums = set(self.nondiff_argnums)
        dyn_argnums = [i for i in range(len(args)) if i not in nondiff_argnums]
        f_, dyn_args = argnums_partial(lu.wrap_init(self.fun), dyn_argnums,
                                       args, require_static_args_hashable=False)
        static_args = [args[i] for i in self.nondiff_argnums]
        fwd, _ = argnums_partial(lu.wrap_init(self.fwd), dyn_argnums, args,
                                 require_static_args_hashable=False)
        bwd = _add_args(lu.wrap_init(self.bwd), static_args)
      else:
        f_, dyn_args = lu.wrap_init(self.fun), args
        fwd, bwd = lu.wrap_init(self.fwd), lu.wrap_init(self.bwd)
      args_flat, in_tree = tree_flatten(dyn_args)
      in_avals = [core.raise_to_shaped(core.get_aval(x)) for x in args_flat]
      flat_fun, out_type = _flatten_fun_nokwargs(f_, in_tree)
      flat_fwd, out_trees = _flatten_fwd(fwd, self.symbolic_zeros, primal_name,
                                         fwd_name, in_tree, out_type)
      flat_bwd = _flatten_bwd(bwd, in_tree, in_avals, out_trees).call_wrapped
      out_flat = custom_vjp_call_p.bind(flat_fun, flat_fwd, flat_bwd,
                                        *args_flat, out_trees=out_trees,
                                        symbolic_zeros=self.symbolic_zeros)
      _, (out_tree, _) = lu.merge_linear_aux(out_type, out_trees)
      return tree_unflatten(out_tree, out_flat)
