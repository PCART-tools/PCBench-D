def needs_check_special() -> bool:
  return config.jax_debug_infs or config.jax_debug_nans
