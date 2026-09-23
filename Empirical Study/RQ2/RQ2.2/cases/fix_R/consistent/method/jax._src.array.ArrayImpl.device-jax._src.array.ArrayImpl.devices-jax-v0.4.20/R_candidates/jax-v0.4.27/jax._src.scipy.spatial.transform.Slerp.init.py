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
