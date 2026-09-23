def _hash_compile_options(hash_obj, compile_options_obj):
  expected_num_compile_options = 12
  # Ignore private and built-in methods. These can unexpectedly change and lead
  # to false positives, e.g. when different Python versions include different
  # built-ins.
  num_actual_options = len(
      [x for x in dir(compile_options_obj) if not x.startswith("_")]
  )
  assert num_actual_options == expected_num_compile_options, (
      "Unexpected number of CompileOption fields: "
      f"{num_actual_options}. This likely: means that an extra "
      "field was added, and this function needs to be updated."
  )

  if compile_options_obj.argument_layouts is not None:
    map(
        lambda shape: hash_obj.update(shape.to_serialized_proto()),
        compile_options_obj.argument_layouts,
    )
  _hash_int(hash_obj, compile_options_obj.parameter_is_tupled_arguments)
  _hash_executable_build_options(
      hash_obj, compile_options_obj.executable_build_options
  )
  _hash_bool(hash_obj, compile_options_obj.tuple_arguments)
  _hash_int(hash_obj, compile_options_obj.num_replicas)
  _hash_int(hash_obj, compile_options_obj.num_partitions)
  _hash_int(hash_obj, compile_options_obj.profile_version)
  if compile_options_obj.device_assignment is not None:
    hash_obj.update(compile_options_obj.device_assignment.serialize())
  _hash_bool(hash_obj, compile_options_obj.compile_portable_executable)
  _hash_int(hash_obj, len(compile_options_obj.env_option_overrides))
  for kv in compile_options_obj.env_option_overrides:
    _hash_string(hash_obj, kv[0])
    if isinstance(kv[1], str):
      _hash_string(hash_obj, kv[1])
    elif isinstance(kv[1], bool):
      _hash_bool(hash_obj, kv[1])
    elif isinstance(kv[1], int):
      _hash_int(hash_obj, kv[1])
    else:
      raise RuntimeError("Invalid type: %s" % repr(type(kv[1])))
