def everything_saveable(*_, **__) -> bool:
  # This is the effective policy without any use of jax.remat.
  return True
