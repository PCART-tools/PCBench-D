  def __init__(self):
    # There are two kinds of value holders: FlagHolders, which hold global
    # flags, and StateContextManagers, which hold state that can be changed
    # locally within a thread. A value holder needs a `.value` property and a
    # `._set()` method.
    self._value_holders = {}
    self.meta = {}
    self.use_absl = False
    self._contextmanager_flags = set()
