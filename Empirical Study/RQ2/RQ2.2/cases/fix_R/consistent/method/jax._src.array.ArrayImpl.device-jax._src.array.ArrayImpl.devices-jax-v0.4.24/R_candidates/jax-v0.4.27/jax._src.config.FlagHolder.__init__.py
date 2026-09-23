  def __init__(self, name: str, default: _T,
               update_hook: Callable[[Any], None] | None = None):
    self._name = name
    self._update_hook = update_hook
    self._set(default)
