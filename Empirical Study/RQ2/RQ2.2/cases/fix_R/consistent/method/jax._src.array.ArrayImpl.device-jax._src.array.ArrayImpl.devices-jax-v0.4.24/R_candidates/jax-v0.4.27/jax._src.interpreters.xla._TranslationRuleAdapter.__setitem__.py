  def __setitem__(self, key: core.Primitive, value: Callable):
    wrapped = self._wrap_fn(key, value)
    for translations in self._translations:
      translations[key] = wrapped
