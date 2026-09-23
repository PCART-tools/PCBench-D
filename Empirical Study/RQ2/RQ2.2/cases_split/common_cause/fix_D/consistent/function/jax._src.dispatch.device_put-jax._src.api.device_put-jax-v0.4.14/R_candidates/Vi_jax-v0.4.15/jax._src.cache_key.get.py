def get(module: ir.Module,
        devices: np.ndarray,
        compile_options: xla_client.CompileOptions,
        backend: xla_client.Client,
        compression_algorithm: str = "zstandard",
        produce_original_cache_key: bool = True) -> str:
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
    produce_original_cache_key: if True, the original cache-key generation
      algorithm is run, else the new one. This is transient; once the migration
      is complete, this parameter and the original algorithm will be removed.
      (New one not implemented as yet.)

  Typical return value example:
   '14ac577cdb2ef6d986078b4054cc9893a9a14a16dbb0d8f37b89167c1f1aacdf'
  """
  entries = []
  if produce_original_cache_key:
    entries = [
        ("computation", lambda hash_obj: _hash_computation(hash_obj, module)),
        ("devices", lambda hash_obj: _hash_devices(hash_obj, devices)),
        ("compile_options",
         lambda hash_obj: _hash_compile_options(hash_obj, compile_options)),
        ("jax_lib version",
         lambda hash_obj: hash_obj.update(
             bytes(jaxlib_version_str.encode("utf-8")))),
        ("the backend", lambda hash_obj: _hash_platform(hash_obj, backend)),
        ("XLA flags",
         lambda hash_obj: _hash_xla_flags(hash_obj, get_flag_prefixes())),
        ("compression",
         lambda hash_obj: _hash_string(hash_obj, compression_algorithm)),
    ]
  else:
    assert False, ("cache_key.get: new cache-key generation algorithm "
                   "not supported as yet.")

  hash_obj = hashlib.sha256()
  for name, hashfn in entries:
    hashfn(hash_obj)
    _log_cache_key_hash(hash_obj, name, hashfn)
  return hash_obj.digest().hex()
