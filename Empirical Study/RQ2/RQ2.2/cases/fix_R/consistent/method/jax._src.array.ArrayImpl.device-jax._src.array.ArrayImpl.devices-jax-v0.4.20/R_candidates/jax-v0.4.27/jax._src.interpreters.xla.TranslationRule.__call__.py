    def __call__(self, ctx: TranslationContext,
                 avals_in: Sequence[core.AbstractValue],
                 avals_out: Sequence[core.AbstractValue],
                 *args: xc.XlaOp, **kw
                ) -> Sequence[xc.XlaOp]:
      """A translation rule lowers a primitive invocation into an XLA HLO."""
