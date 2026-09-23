  def reset(self):
    _profile_state.profile_session = None
    _profile_state.create_perfetto_link = False
    _profile_state.create_perfetto_trace = False
    _profile_state.log_dir = None
