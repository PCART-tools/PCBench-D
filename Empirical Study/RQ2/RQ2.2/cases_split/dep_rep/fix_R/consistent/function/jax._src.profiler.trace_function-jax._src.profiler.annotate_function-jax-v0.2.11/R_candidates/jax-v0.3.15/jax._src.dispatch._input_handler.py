def _input_handler(backend: Backend,
                   in_type: Optional[pe.InputType],
                   out_type: Optional[pe.OutputType],
                   ) -> Optional[Callable]:
  if in_type is None:
    assert out_type is None
    return None
  in_avals, which_explicit = util.unzip2(in_type)
  # Check whether we actually need an input_handler.
  needs_implicit = which_explicit and not all(which_explicit)
  needs_out_handling = any(type(d) is core.InDBIdx for a, _ in out_type or []
                           if type(a) is core.DShapedArray for d in a.shape)

  if not needs_implicit and not needs_out_handling:
    return None
  assert config.jax_dynamic_shapes

  # Precompute how to grab implicit inputs from explicit inputs' axis sizes.
  which_explicit = which_explicit or [True] * len(in_avals)
  implicit_idxs = {i for i, ex in enumerate(which_explicit) if not ex}
  implicit_args_from_axes: List[Tuple[int, int, int]] = []
  for arg_idx, aval in enumerate(in_avals):
    if isinstance(aval, core.DShapedArray):
      for axis_idx, d in enumerate(aval.shape):
        if isinstance(d, core.DBIdx) and d.val in implicit_idxs:
          implicit_args_from_axes.append((d.val, arg_idx, axis_idx))
  assert {i for i, _, _ in implicit_args_from_axes} == implicit_idxs

  # Precompute which input values are needed for output types.
  inputs_needed_for_out_types = out_type and [
      d.val for aval, _ in out_type if type(aval) is core.DShapedArray  # type: ignore
      for d in aval.shape if type(d) is core.InDBIdx]

  def elaborate(explicit_args: Sequence[Any]) -> Tuple[Tuple, Optional[Tuple]]:
    if needs_implicit:
      # Build full argument list, leaving Nones for implicit arguments.
      explicit_args_ = iter(explicit_args)
      args = [next(explicit_args_) if ex else None for ex in which_explicit]
      assert next(explicit_args_, None) is None
      # Populate implicit arguments.
      for i, j, k in implicit_args_from_axes:
        if args[i] is None:
          args[i] = args[j].shape[k]  # type: ignore
        else:
          if args[i] != args[j].shape[k]:
            raise Exception("inconsistent argument axis sizes for type")
    else:
      args = list(explicit_args)

    if needs_out_handling:
      # Make a list of inputs needed by output types, leaving unneeded as None.
      out_type_env = [None] * len(args)
      for i in inputs_needed_for_out_types or []:
        out_type_env[i] = args[i]
    else:
      out_type_env = None  # type: ignore

    return tuple(args), out_type_env and tuple(out_type_env)  # type: ignore
  return elaborate
