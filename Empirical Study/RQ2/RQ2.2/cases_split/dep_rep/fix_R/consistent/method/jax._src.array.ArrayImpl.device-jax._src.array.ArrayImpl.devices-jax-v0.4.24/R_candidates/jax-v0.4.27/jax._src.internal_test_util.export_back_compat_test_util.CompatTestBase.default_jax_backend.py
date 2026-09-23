  def default_jax_backend(self) -> str:
    # Canonicalize to turn into "cuda" or "rocm"
    return xb.canonicalize_platform(jax.default_backend())
