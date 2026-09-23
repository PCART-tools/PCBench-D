def _make_tpu_driver_client():
  if tpu_driver_client is None:
    logger.info("Remote TPU is not linked into jax; skipping remote TPU.")
    return None
  if FLAGS.jax_backend_target is None:
    logger.info("No --jax_backend_target was provided; skipping remote TPU.")
    return None
  return tpu_driver_client.TpuBackend.create(worker=FLAGS.jax_backend_target)
