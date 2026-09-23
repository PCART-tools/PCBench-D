def get_cache_key(module: ir.Module, devices: np.ndarray, compile_options,
                  backend) -> str:
  return cache_key.get(module, devices, compile_options, backend,
                       "zstandard" if zstandard is not None else "zlib")
