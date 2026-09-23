class DeviceIdSet:
  _name: str
  _ids: frozenset[int]
  def __init__(self, name, *ids):
    self._name = name
    self._ids = frozenset(ids)

  def __iter__(self):
    return iter(sorted(self._ids))

  def __add__(self, other) -> DeviceIdSet:
    assert isinstance(other, DeviceIdSet)
    return DeviceIdSet(self._name, *(self._ids | other._ids))

  def __len__(self) -> int:
    return len(self._ids)

  def __repr__(self) -> str:
    ids = ', '.join(safe_map(str, sorted(self._ids)))
    return f'{{{self._name} {ids}}}'

  def __hash__(self) -> int:
    return hash((self._name, self._ids))

  def __eq__(self, other) -> bool:
    return (isinstance(other, DeviceIdSet) and self._name == other._name and
            self._ids == other._ids)
