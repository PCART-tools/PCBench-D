class _SourceInfoContext(threading.local):
  context: SourceInfo

  def __init__(self):
    self.context = new_source_info()
