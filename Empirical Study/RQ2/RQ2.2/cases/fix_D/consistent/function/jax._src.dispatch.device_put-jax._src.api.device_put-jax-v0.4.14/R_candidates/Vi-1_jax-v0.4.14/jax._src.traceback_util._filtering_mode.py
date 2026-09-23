def _filtering_mode() -> str:
  mode = config.jax_traceback_filtering
  if mode is None or mode == "auto":
    if (_running_under_ipython() and _ipython_supports_tracebackhide()):
      mode = "tracebackhide"
    else:
      mode = "remove_frames"
  return mode
