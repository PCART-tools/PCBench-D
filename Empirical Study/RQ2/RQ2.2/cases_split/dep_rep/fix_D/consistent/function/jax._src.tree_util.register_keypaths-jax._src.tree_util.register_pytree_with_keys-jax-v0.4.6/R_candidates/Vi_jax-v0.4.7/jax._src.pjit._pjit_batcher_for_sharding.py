def _pjit_batcher_for_sharding(
    s: Union[GSPMDSharding, _UnspecifiedValue],
    dim: int, val: Tuple[str, ...], mesh, ndim: int):
  if _is_unspecified(s):
    return s
  if not val:
    new_op = s._op_sharding.clone()  # type: ignore
    tad = list(new_op.tile_assignment_dimensions)
    tad.insert(dim, 1)
    new_op.tile_assignment_dimensions = tad
    return GSPMDSharding(s._device_assignment, new_op)  # type: ignore
  else:
    assert isinstance(s, GSPMDSharding)
    assert mesh is not None and not mesh.empty
    parsed_pspec = parse_flatten_op_sharding(s._op_sharding, mesh)[0]  # type: ignore
    parsed_pspec = parsed_pspec.insert_axis_partitions(dim, val)
    mps = NamedSharding._from_parsed_pspec(mesh, parsed_pspec)
    return GSPMDSharding(mps._device_assignment, mps._to_xla_op_sharding(ndim))
