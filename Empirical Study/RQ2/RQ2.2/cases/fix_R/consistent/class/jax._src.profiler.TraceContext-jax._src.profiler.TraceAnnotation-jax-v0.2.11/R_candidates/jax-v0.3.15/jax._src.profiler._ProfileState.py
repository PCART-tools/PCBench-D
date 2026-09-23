class _ProfileState:
  def __init__(self):
    self.profile_session = None
    self.log_dir = None
    self.create_perfetto_link = False
    self.lock = threading.Lock()
