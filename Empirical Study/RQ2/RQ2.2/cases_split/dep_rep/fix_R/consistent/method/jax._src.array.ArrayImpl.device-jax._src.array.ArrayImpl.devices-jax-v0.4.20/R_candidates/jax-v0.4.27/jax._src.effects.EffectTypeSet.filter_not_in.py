  def filter_not_in(self, effects: Iterable[Effect]) -> list[Effect]:
    return [eff for eff in effects if not self.contains(eff)]
