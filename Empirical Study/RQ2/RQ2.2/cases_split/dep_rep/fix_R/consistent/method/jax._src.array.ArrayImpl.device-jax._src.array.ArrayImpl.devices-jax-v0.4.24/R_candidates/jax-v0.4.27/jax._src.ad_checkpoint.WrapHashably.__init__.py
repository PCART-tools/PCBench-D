  def __init__(self, val):
    self.val = val
    try:
      self.hash = hash(val)
      self.hashable = True
    except:
      self.hash = id(val)
      self.hashable = False
