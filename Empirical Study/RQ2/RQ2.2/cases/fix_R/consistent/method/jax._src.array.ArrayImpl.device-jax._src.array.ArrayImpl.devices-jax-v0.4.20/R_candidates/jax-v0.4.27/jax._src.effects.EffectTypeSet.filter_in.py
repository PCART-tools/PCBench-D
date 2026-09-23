  def filter_in(self, effects: Iterable[Effect]) -> list[Effect]:
    return [eff for eff in effects if self.contains(eff)]
