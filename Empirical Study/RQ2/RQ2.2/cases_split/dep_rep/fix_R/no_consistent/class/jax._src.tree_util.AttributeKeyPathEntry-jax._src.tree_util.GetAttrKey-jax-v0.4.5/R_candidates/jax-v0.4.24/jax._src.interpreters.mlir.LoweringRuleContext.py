@dataclasses.dataclass
class LoweringRuleContext:
  """Per-rule context information for MLIR lowering."""
  module_context: ModuleContext
  primitive: core.Primitive | None
  avals_in: Sequence[core.AbstractValue]
  avals_out: Any  # Usually Sequence[core.AbstractValue], but sometimes None.
  tokens_in: TokenSet
  tokens_out: TokenSet | None  # Mutable store for output containers
  axis_size_env: dict[core.Var, ir.Value] | None = None  # Dynamic axis sizes
  dim_var_values: Sequence[ir.Value] = ()  # The values for the dimension variables
                                           # in same order as module_context.shape_poly_state.dim_vars

  def set_tokens_out(self, tokens_out: TokenSet):
    assert self.tokens_out is None, 'Should only set `tokens_out` once.'
    self.tokens_out = tokens_out

  def replace(self, **kw): return dataclasses.replace(self, **kw)
