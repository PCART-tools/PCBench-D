def _register_handlers_for_sharded_device_array(sda):
  shard_arg_handlers[sda] = shard_sharded_device_array_slow_path
  mlir.register_constant_handler(sda,
                                 _sharded_device_array_mlir_constant_handler)

  core.pytype_aval_mappings[sda] = abstract_arrays.canonical_concrete_aval
  xla.pytype_aval_mappings[sda] = op.attrgetter("aval")
  xla.canonicalize_dtype_handlers[sda] = identity
  api_util._shaped_abstractify_handlers[sda] = op.attrgetter("aval")
