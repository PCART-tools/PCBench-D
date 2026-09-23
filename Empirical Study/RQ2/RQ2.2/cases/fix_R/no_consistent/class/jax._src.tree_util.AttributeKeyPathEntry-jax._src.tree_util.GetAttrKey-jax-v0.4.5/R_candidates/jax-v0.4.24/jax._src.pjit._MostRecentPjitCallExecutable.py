class _MostRecentPjitCallExecutable(threading.local):
  def __init__(self):
    self.weak_key_dict = weakref.WeakKeyDictionary()
