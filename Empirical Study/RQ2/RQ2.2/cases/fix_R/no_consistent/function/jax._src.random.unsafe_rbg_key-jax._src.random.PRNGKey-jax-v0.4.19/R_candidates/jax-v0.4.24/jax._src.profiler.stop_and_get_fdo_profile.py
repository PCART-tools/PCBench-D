def stop_and_get_fdo_profile() -> bytes:
  """Stops the currently-running profiler trace and export fdo_profile.

  Currently, this is only supported for GPU.
  Raises a RuntimeError if a trace hasn't been started.
  """
  with _profile_state.lock:
    if _profile_state.profile_session is None:
      raise RuntimeError("No profile started")
    xspace = _profile_state.profile_session.stop()
    fdo_profile = xla_client.profiler.get_fdo_profile(xspace)
    _profile_state.reset()
    return fdo_profile
