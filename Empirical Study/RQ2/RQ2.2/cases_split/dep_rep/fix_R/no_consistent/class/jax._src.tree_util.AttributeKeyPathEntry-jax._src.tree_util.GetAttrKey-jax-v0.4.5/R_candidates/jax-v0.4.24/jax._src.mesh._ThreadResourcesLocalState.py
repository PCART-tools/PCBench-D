class _ThreadResourcesLocalState(threading.local):

  def __init__(self):
    self.stack = [EMPTY_ENV]
    self.env = self.stack[-1]
