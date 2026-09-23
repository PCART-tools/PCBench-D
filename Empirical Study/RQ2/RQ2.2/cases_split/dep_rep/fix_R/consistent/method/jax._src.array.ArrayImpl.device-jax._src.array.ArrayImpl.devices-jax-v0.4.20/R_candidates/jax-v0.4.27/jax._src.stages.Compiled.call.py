  @staticmethod
  def call(*args, **kwargs):
    # This is because `__call__` passes in `self._params` as the first argument.
    # Instead of making the call signature `call(params, *args, **kwargs)`
    # extract it from args because `params` can be passed as a kwarg by users
    # which might conflict here.
    params = args[0]
    args = args[1:]
    if config.dynamic_shapes.value:
      raise NotImplementedError
    if params.no_kwargs and kwargs:
      kws = ', '.join(kwargs.keys())
      raise NotImplementedError(
          "function was compiled by a transformation that does not support "
          f"keyword arguments, but called with keyword arguments: {kws}")
    args_flat, in_tree = tree_util.tree_flatten((args, kwargs))
    if in_tree != params.in_tree:
      leaf = PytreeLeaf()
      this_dummy = tree_unflatten(in_tree, [leaf] * in_tree.num_leaves)
      other_dummy = tree_unflatten(
          params.in_tree, [leaf] * params.in_tree.num_leaves)  # type: ignore
      errs = list(tree_util.equality_errors(this_dummy, other_dummy))
      msg = []
      msg.append(
          "Function compiled with input pytree does not match the input pytree"
          f" it was called with. There are {len(errs)} mismatches, including:")
      for path, thing1, thing2, explanation in errs:
        fst, *rest = path  # type: ignore
        base = ['args', 'kwargs'][fst.idx]
        msg.append(
            f"    * at {base}{keystr(rest)}, seen {thing2} but now given"  # type: ignore
            f" {thing1}, so {explanation}")
      raise TypeError('\n'.join(msg))
    try:
      out_flat = params.executable.call(*args_flat)
    except TypeError as e:
      # We can't transform ahead-of-time compiled calls, since we've
      # lowered and compiled for a fixed function signature, and JAX
      # transformations change signatures. We interpret a Tracer
      # argument as an indication of a transformation attempt. We
      # could check this before the executable call, but we'd rather
      # avoid isinstance checks on the call path. Seeing a TypeError
      # might mean that arguments have JAX-invalid types, which in
      # turn might mean some are Tracers.
      for arg in args_flat:
        if isinstance(arg, core.Tracer):
          raise TypeError(
              "Cannot apply JAX transformations to a function lowered and "
              "compiled for a particular signature. Detected argument of "
              f"Tracer type {type(arg)}.") from e
      else:
        raise
    outs = tree_util.tree_unflatten(params.out_tree, out_flat)
    return outs, out_flat, args_flat
