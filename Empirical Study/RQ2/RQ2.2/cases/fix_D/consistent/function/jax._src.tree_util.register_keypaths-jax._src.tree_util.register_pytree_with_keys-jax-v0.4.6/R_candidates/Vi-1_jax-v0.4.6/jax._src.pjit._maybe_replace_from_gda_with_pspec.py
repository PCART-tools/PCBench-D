def _maybe_replace_from_gda_with_pspec(
    in_shardings_flat, args_flat) -> Sequence[XLACompatibleSharding]:

  @lru_cache()
  def _gda_check_and_get_sharding(
      gda_sharding: NamedSharding, in_sharding: GSPMDSharding, ndim: int):
    if not _is_from_gda(in_sharding) and not pxla.are_op_shardings_equal(
        gda_sharding._to_xla_op_sharding(ndim),
        in_sharding._to_xla_op_sharding(ndim)):
      raise ValueError(
          f"Got an input GDA to pjit with different partitioning than specified in "
          "the in_axis_resources argument to pjit. The partitioning must match, or "
          "use `jax.experimental.pjit.FROM_GDA` in `in_axis_resources` for GDA. "
          f"Got GDA sharding: {gda_sharding} and "
          f"pjit sharding: {in_sharding._original_sharding}")  # type: ignore
    return to_gspmd_sharding(gda_sharding, ndim)

  out = []
  for in_sharding_flat, arg in safe_zip(in_shardings_flat, args_flat):
    if is_auto(in_sharding_flat):
      out.append(in_sharding_flat)
    elif isinstance(arg, array.ArrayImpl):
      out.append(to_gspmd_sharding(arg.sharding, arg.ndim))
    elif isinstance(arg, GDA):
      gda_sharding = pxla.create_mesh_pspec_sharding(arg.mesh, arg.mesh_axes)
      out.append(_gda_check_and_get_sharding(gda_sharding, in_sharding_flat, arg.ndim))
    else:
      out.append(in_sharding_flat)
  return tuple(out)
