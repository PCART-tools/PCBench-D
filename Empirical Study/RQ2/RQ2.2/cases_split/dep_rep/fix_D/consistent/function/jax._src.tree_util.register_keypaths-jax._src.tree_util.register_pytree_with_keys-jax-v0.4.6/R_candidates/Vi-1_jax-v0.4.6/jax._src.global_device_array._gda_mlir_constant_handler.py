def _gda_mlir_constant_handler(val, canonicalize_types=True):
  return mlir.ir_constants(val._value,
                           canonicalize_types=canonicalize_types)
