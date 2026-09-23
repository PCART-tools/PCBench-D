  def mhlo(self) -> ir.Module:
    """Return an MHLO representation of this computation."""
    warnings.warn(
        "mhlo support is deprecated and will be removed "
        "from a future release of JAX. Use stablehlo instead.",
        DeprecationWarning,
    )
    module_str = xla_extension.mlir.stablehlo_to_mhlo(
        mlir.module_to_bytecode(self.stablehlo()))
    with self.stablehlo().context:
      return ir.Module.parse(module_str)
