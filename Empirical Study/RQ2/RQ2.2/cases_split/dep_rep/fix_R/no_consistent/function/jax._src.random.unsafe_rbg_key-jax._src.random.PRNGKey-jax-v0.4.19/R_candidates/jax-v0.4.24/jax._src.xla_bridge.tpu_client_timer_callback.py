def tpu_client_timer_callback(timer_secs: float) -> xla_client.Client | None:
  def _log_warning():
    warnings.warn(
      f'TPU backend initialization is taking more than {timer_secs} seconds. '
      'Did you run your code on all TPU hosts? '
      'See https://jax.readthedocs.io/en/latest/multi_process.html '
      'for more information.')

  # Will log a warning after `timer_secs`.
  t = threading.Timer(timer_secs, _log_warning)
  t.start()

  try:
    client = xla_client.make_tpu_client(_get_tpu_library_path())
  finally:
    t.cancel()

  return client
