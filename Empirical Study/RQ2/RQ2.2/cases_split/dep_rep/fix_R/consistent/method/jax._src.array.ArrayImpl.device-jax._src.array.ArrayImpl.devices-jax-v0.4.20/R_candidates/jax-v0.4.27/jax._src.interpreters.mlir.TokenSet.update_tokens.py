  def update_tokens(self, tokens: TokenSet) -> TokenSet:
    """Returns a new `TokenSet` with tokens replaced with ones from the input `TokenSet`."""
    new_tokens = []
    for eff in self.effects():
      if eff in tokens._tokens:
        new_tokens.append((eff, tokens._tokens[eff]))
      else:
        new_tokens.append((eff, self._tokens[eff]))
    return TokenSet(new_tokens)
