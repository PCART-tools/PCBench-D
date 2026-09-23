  @property
  def values(self):
    return {name: holder.value for name, holder in self._value_holders.items()}
