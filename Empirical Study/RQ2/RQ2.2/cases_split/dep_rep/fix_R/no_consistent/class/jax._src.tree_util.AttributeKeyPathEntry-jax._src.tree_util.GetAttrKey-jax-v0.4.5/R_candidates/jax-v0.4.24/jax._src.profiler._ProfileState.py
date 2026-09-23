class _ProfileState:
  def __init__(self):
    self.profile_session = None
    self.log_dir = None
    self.create_perfetto_link = False
    self.create_perfetto_trace = False
    self.lock = threading.Lock()

  def reset(self):
    _profile_state.profile_session = None
    _profile_state.create_perfetto_link = False
    _profile_state.create_perfetto_trace = False
    _profile_state.log_dir = None
