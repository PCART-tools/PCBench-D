  def items(self) -> Sequence[tuple[core.Effect, Token]]:
    return tuple(self._tokens.items())
