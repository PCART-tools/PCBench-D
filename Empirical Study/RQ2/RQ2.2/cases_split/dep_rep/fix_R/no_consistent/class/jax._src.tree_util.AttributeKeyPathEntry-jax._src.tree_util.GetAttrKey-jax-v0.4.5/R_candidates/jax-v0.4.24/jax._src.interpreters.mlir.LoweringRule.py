  class LoweringRule(Protocol):
    def __call__(self, ctx: LoweringRuleContext,
                 *args: ir.Value | Sequence[ir.Value],
                 **kw) -> Sequence[ir.Value | Sequence[ir.Value]]:
      """Converts a JAX primitive invocation into MLIR."""
