  def contains(self, eff: Effect) -> bool:
    return any(isinstance(eff, eff_type) for eff_type in self._effect_types)
