def filtering_mode():
  mode = jax.config.jax_traceback_filtering
  if mode is None or mode == "auto":
    if (running_under_ipython() and ipython_supports_tracebackhide()):
      mode = "tracebackhide"
    else:
      mode = "remove_frames"
  return mode
