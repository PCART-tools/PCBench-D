class EqualStore:
  __slots__ = ('_store',)

  def __init__(self):
    self._store = Store()

  val = property(operator.attrgetter('_store.val'))

  def store(self, val):
    try:
      self._store.store(val)
    except StoreException as e:
      try:
        okay = bool(self._store._val == val)
      except:
        raise e from None
      else:
        if not okay:
          raise StoreException("Store occupied with not-equal value") from None

  def reset(self):
    self._store.reset()
