  def hlo(self) -> xc.XlaComputation:
    """Return an HLO representation of this computation."""
    hlo = self.stablehlo()
    m: Union[str, bytes]
    if xla_extension_version >= 244:
      m = mlir.module_to_bytecode(hlo)
    else:
      m = mlir.module_to_string(hlo)
    return xla_extension.mlir.mlir_module_to_xla_computation(
        m, use_tuple_args=self.compile_args["tuple_args"])
