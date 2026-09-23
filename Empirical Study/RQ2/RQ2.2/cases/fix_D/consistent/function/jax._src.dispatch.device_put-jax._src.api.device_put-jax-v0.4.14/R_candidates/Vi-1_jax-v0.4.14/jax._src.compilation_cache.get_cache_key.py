def get_cache_key(module: ir.Module, devices: np.ndarray, compile_options,
                  backend) -> str:
  """Creates a hashed string to use as a key to the compilation cache.

  get_cache_key takes in the MLIR module and compile_options of a program
  and hashes all the components into a unique hash. The hash is returned as a
  hex-encoded string that is 256 characters long.

  Typical return value example:
   '14ac577cdb2ef6d986078b4054cc9893a9a14a16dbb0d8f37b89167c1f1aacdf'
  """
  entries = [
    ("computation", lambda hash_obj: _hash_computation(hash_obj, module)),
    ("devices", lambda hash_obj: _hash_devices(hash_obj, devices)),
    ("compile_options",
     lambda hash_obj: _hash_compile_options(hash_obj, compile_options)),
    ("jax_lib version",
     lambda hash_obj: hash_obj.update(bytes(jaxlib_version_str.encode("utf-8")))
    ),
    ("the backend", lambda hash_obj: _hash_platform(hash_obj, backend)),
    ("XLA flags", _hash_xla_flags),
    ("compression", _hash_compression),
  ]

  hash_obj = hashlib.sha256()
  for name, hashfn in entries:
    hashfn(hash_obj)
    _log_cache_key_hash(hash_obj, name, hashfn)
  return hash_obj.digest().hex()
