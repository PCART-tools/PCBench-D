def _sharded_device_array_mlir_constant_handler(val, canonicalize_types=True):
  return mlir.ir_constants(np.asarray(val),
                           canonicalize_types=canonicalize_types)
