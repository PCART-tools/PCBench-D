def _pjit_batcher_for_sharding(
    s: Union[GSPMDSharding, UnspecifiedValue],
    dim: int, val: tuple[str, ...], mesh, ndim: int):
  if is_unspecified(s):
    return s
  if not val:
    if sharding_impls.is_op_sharding_replicated(s._hlo_sharding):  # type: ignore
      return s
    old_op = s._hlo_sharding.to_proto()  # type: ignore
    new_op = old_op.clone()  # type: ignore
    tad = list(new_op.tile_assignment_dimensions)
    tad.insert(dim, 1)
    new_op.tile_assignment_dimensions = tad
    new_gs = GSPMDSharding(s._device_assignment, new_op)  # type: ignore
    if hasattr(s, '_original_sharding'):
      vmapped_s, _ = pxla._get_out_sharding_from_orig_sharding(
          [new_gs], [None], s._original_sharding, None, [False])[0]  # type: ignore
      new_gs = to_gspmd_sharding(vmapped_s, ndim)
    return new_gs
  else:
    assert isinstance(s, GSPMDSharding)
    if isinstance(getattr(s, '_original_sharding', None), NamedSharding):
      mesh = s._original_sharding.mesh  # type: ignore
    assert mesh is not None and not mesh.empty
    parsed_pspec = parse_flatten_op_sharding(s._hlo_sharding, mesh)[0]  # type: ignore
    parsed_pspec = parsed_pspec.insert_axis_partitions(dim, val)
    mps = NamedSharding._from_parsed_pspec(mesh, parsed_pspec)
    return GSPMDSharding(mps._device_assignment, mps._to_xla_hlo_sharding(ndim))
