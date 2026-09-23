def get(module: ir.Module,
        devices: np.ndarray,
        compile_options: xla_client.CompileOptions,
        backend: xla_client.Client,
        compression_algorithm: str = "zstandard") -> str:
  """Creates a hashed string to use as a key to the compilation cache.

  Creates a cache key that is a hex-encoded string of a unique hash based on
  the arguments. The hex-encoded string is 256 characters long.

  Args:
    module: the input program
    devices: an array of accelerator devices that the program will run on
    compile_options: options passed to the XLA compiler
    backend: description of the platform (e.g., TPU version)
    compression_algorithm: a string representing the compression algorithm used
      for the executable before persisting in the cache

  Typical return value example:
   'jit__psum-14ac577cdb2ef6d986078b4054cc9893a9a14a16dbb0d8f37b89167c1f1aacdf'
  """
  entries = [
      ("computation", lambda hash_obj: _hash_computation(hash_obj, module)),
      ("jax_lib version",
       lambda hash_obj: hash_obj.update(
           bytes(jaxlib_version_str.encode("utf-8")))),
      ("XLA flags",
       lambda hash_obj: _hash_xla_flags(hash_obj, get_flag_prefixes())),
      ("compile_options",
       lambda hash_obj: _hash_serialized_compile_options(
           hash_obj, compile_options)),
      ("accelerator_config",
         lambda hash_obj: _hash_accelerator_config(hash_obj, devices, backend)),
      ("compression",
       lambda hash_obj: _hash_string(hash_obj, compression_algorithm)),
  ]

  hash_obj = hashlib.sha256()
  for name, hashfn in entries:
    hashfn(hash_obj)
    _log_cache_key_hash(hash_obj, name, hashfn)
  sym_name = module.operation.attributes['sym_name']
  module_name = ir.StringAttr(sym_name).value
  return module_name + "-" + hash_obj.digest().hex()
