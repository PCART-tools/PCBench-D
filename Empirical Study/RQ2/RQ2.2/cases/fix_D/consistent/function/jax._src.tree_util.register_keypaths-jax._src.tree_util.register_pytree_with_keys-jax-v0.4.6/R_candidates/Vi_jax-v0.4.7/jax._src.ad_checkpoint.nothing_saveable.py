def nothing_saveable(*_, **__) -> bool:
  # This is the effective policy when using jax.remat without explicit policy.
  return False
