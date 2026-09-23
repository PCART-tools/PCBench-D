def infer_lambda_input_type(
    axes_specs: Sequence[AbstractedAxesSpec] | None,
    args: Sequence[Any]
  ) -> InputType:
  ndims = [getattr(get_aval(x), 'ndim', 0) for x in args]
  partial_specs = _canonicalize_specs(ndims, axes_specs)
  specs = _complete_specs(args, partial_specs)
  idxs, implicit_types = _collect_implicit(args, specs)
  implicit_sig = [(ty, False) for ty in implicit_types]
  explicit_sig = [(_arg_type(idxs, x, s), True) for x, s in zip(args, specs)]
  input_type = (*implicit_sig, *explicit_sig)
  lu._check_input_type(input_type)
  return input_type
