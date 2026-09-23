def start_trace(log_dir, create_perfetto_link: bool = False):
  """Starts a profiler trace.

  The trace will capture CPU, GPU, and/or TPU activity, including Python
  functions and JAX on-device operations. Use ``stop_trace()`` to end the trace
  and save the results to ``log_dir``.

  The resulting trace can be viewed with TensorBoard. Note that TensorBoard
  doesn't need to be running when collecting the trace.

  Only once trace may be collected a time. A RuntimeError will be raised if
  ``start_trace()`` is called while another trace is running.

  Args:
    log_dir: The directory to save the profiler trace to (usually the
      TensorBoard log directory).
    create_perfetto_link: A boolean which, if true, creates and prints link to
      the Perfetto trace viewer UI (https://ui.perfetto.dev). The program will
      block until the link is opened and Perfetto loads the trace.
  """
  with _profile_state.lock:
    if _profile_state.profile_session is not None:
      raise RuntimeError("Profile has already been started. "
                         "Only one profile may be run at a time.")
    # Make sure backends are initialized before creating a profiler
    # session. Otherwise on Cloud TPU, libtpu may not be initialized before
    # creating the tracer, which will cause the TPU tracer initialization to
    # fail and no TPU operations will be included in the profile.
    xla_bridge.get_backend()

    _profile_state.profile_session = xla_client.profiler.ProfilerSession()
    _profile_state.create_perfetto_link = create_perfetto_link
    _profile_state.log_dir = log_dir
