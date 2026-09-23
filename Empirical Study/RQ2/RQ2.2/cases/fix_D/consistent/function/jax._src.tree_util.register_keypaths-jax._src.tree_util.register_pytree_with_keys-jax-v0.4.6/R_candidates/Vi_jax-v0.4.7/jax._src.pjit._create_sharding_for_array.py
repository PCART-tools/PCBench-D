def _create_sharding_for_array(mesh, x):
  # TODO(yashkatariya): Only check for auto and unspecified here after
  # FROM_GDA is removed.
  if isinstance(x, XLACompatibleSharding) or _is_unspecified_or_from_gda_or_auto(x):
    return x
  if mesh is None:
    raise RuntimeError(
        "jit does not support using the mesh context manager and passing "
        "PartitionSpecs to in_shardings or out_shardings. Please pass in "
        "the `Sharding` explicitly via in_shardings or out_shardings.")
  if mesh.empty:
    raise RuntimeError(
        'pjit requires a non-empty mesh if you are passing `PartitionSpec`s or'
        ' `None` to in_shardings or out_shardings! Is a mesh defined at the'
        ' call site? Alternatively, provide `XLACompatibleSharding`s to'
        ' `in_shardings` and `out_shardings` and then the mesh context manager'
        ' is not required.')
  # A nice user error is raised in _prepare_axis_resources.
  assert isinstance(x, ParsedPartitionSpec), x
  return _create_mesh_pspec_sharding_from_parsed_pspec(mesh, x)
