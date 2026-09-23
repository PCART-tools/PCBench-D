class EffectTypeSet:

  def __init__(self):
    self._effect_types: set[type[Effect]] = set()

  def add_type(self, effect_type: type[Effect]):
    self._effect_types.add(effect_type)

  def contains(self, eff: Effect) -> bool:
    return any(isinstance(eff, eff_type) for eff_type in self._effect_types)

  def filter_in(self, effects: Iterable[Effect]) -> list[Effect]:
    return [eff for eff in effects if self.contains(eff)]

  def filter_not_in(self, effects: Iterable[Effect]) -> list[Effect]:
    return [eff for eff in effects if not self.contains(eff)]
