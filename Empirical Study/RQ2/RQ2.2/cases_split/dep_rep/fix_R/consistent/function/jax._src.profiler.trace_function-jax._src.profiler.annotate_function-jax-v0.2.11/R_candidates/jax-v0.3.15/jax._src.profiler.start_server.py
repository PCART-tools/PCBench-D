def start_server(port: int):
  """Starts the profiler server on port `port`.

  Using the "TensorFlow profiler" feature in `TensorBoard
  <https://www.tensorflow.org/tensorboard>`_ 2.2 or newer, you can
  connect to the profiler server and sample execution traces that show CPU,
  GPU, and/or TPU device activity.
  """
  global _profiler_server
  if _profiler_server is not None:
    raise ValueError("Only one profiler server can be active at a time.")

  # Make sure backends are initialized before creating a profiler
  # session. Otherwise on Cloud TPU, libtpu may not be initialized before
  # creating the tracer, which will cause the TPU tracer initialization to
  # fail and no TPU operations will be included in the profile.
  # NOTE(skyewm): I'm not sure this is necessary for start_server (is definitely
  # is for start_trace), but I'm putting it here to be safe.
  xla_bridge.get_backend()

  _profiler_server = xla_client.profiler.start_server(port)
  return _profiler_server
