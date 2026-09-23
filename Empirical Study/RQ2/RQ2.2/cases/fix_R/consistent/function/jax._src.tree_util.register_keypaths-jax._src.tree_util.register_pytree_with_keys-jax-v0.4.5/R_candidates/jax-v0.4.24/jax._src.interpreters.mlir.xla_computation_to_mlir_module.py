def xla_computation_to_mlir_module(xla_computation: xc.XlaComputation
                                  ) -> ir.Module:
  module_str = xc._xla.mlir.xla_computation_to_mlir_module(xla_computation)
  return ir.Module.parse(module_str)
