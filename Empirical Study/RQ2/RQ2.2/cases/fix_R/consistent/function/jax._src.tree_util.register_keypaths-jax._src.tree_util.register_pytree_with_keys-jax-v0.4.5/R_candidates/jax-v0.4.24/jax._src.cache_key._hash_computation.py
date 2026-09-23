def _hash_computation(hash_obj, module):
  if config.compilation_cache_include_metadata_in_key.value:
    canonical_ir = _serialize_ir(module)
  else:
    canonical_ir = _canonicalize_ir(module)
  hash_obj.update(canonical_ir)
