  def __call__(self, times: jax.Array):
    """Interpolate rotations."""
    compute_times = jnp.asarray(times, dtype=self.times.dtype)
    if compute_times.ndim > 1:
      raise ValueError("`times` must be at most 1-dimensional.")
    single_time = compute_times.ndim == 0
    compute_times = jnp.atleast_1d(compute_times)
    ind = jnp.maximum(jnp.searchsorted(self.times, compute_times) - 1, 0)
    alpha = (compute_times - self.times[ind]) / self.timedelta[ind]
    result = (self.rotations[ind] * Rotation.from_rotvec(self.rotvecs[ind] * alpha[:, None]))
    if single_time:
      return result[0]
    return result
