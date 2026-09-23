@implements(scipy.spatial.transform.Slerp)
class Slerp(typing.NamedTuple):
  """Spherical Linear Interpolation of Rotations."""

  times: jnp.ndarray
  timedelta: jnp.ndarray
  rotations: Rotation
  rotvecs: jnp.ndarray

  @classmethod
  def init(cls, times: jax.Array, rotations: Rotation):
    if not isinstance(rotations, Rotation):
      raise TypeError("`rotations` must be a `Rotation` instance.")
    if rotations.single or len(rotations) == 1:
      raise ValueError("`rotations` must be a sequence of at least 2 rotations.")
    times = jnp.asarray(times, dtype=rotations.quat.dtype)
    if times.ndim != 1:
      raise ValueError("Expected times to be specified in a 1 "
                       "dimensional array, got {} "
                       "dimensions.".format(times.ndim))
    if times.shape[0] != len(rotations):
      raise ValueError("Expected number of rotations to be equal to "
                       "number of timestamps given, got {} rotations "
                       "and {} timestamps.".format(len(rotations), times.shape[0]))
    timedelta = jnp.diff(times)
    # if jnp.any(timedelta <= 0):  # this causes a concretization error...
    #   raise ValueError("Times must be in strictly increasing order.")
    new_rotations = Rotation(rotations.as_quat()[:-1])
    return cls(
      times=times,
      timedelta=timedelta,
      rotations=new_rotations,
      rotvecs=(new_rotations.inv() * Rotation(rotations.as_quat()[1:])).as_rotvec())

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
