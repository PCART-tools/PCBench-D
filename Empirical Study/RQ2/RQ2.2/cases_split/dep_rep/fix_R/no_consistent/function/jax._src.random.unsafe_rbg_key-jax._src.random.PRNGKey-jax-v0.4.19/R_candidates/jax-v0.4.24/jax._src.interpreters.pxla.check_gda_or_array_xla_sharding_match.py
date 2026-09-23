def check_gda_or_array_xla_sharding_match(
    args, in_xla_shardings: Sequence[sharding_impls.XLACompatibleSharding],
    jaxpr_debug_info: core.JaxprDebugInfo | None) -> None:
  from jax._src.array import ArrayImpl
  arg_names = ([''] * len(args) if jaxpr_debug_info is None else
               jaxpr_debug_info.arg_names)
  errors = []
  num_errors = 5
  for arg, xs, name in safe_zip(args, in_xla_shardings, arg_names):
    if not isinstance(arg, ArrayImpl):
      continue
    if is_unspecified_or_auto(xs):
      continue

    db_xs = check_device_backend_on_shardings([xs])
    if not db_xs:
      xs = getattr(xs, '_original_sharding', xs)

    # Raise memory kind mismatch error even if the arg is uncommitted.
    if arg.sharding.memory_kind != xs.memory_kind:
      errors.append(
          "Got input sharding(s) that compiled object was called with: "
          f"{arg.sharding} and sharding(s) the computation was compiled "
          f"with: {xs} for arg {name} with shape: {arg.aval.str_short()}")

    if (not db_xs and arg._committed and
        not op_shardings.are_op_shardings_equal(
            arg.sharding._to_xla_hlo_sharding(arg.ndim),
            xs._to_xla_hlo_sharding(arg.ndim))):
      errors.append(
          "Got input sharding(s) that compiled object was called with: "
          f"{arg.sharding} and sharding(s) the computation was compiled "
          f"with: {xs} for arg {name} with shape: {arg.aval.str_short()}")

  if errors:
    str_errors = '\n'.join(errors[:num_errors])
    num_mismatch_str = (
        f'the {len(errors)} mismatches' if len(errors) < num_errors else
        f"{num_errors} mismatches out of {len(errors)}")
    raise ValueError(
          "Compiled object called with input sharding(s) does not match the "
          "sharding(s) the computation was compiled with. "
          f"Here are {num_mismatch_str}:\n{str_errors}")
