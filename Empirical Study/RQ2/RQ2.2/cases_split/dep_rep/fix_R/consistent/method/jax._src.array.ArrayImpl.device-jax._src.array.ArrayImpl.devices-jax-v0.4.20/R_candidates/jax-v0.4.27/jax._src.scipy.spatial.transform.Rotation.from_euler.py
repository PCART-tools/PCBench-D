  @classmethod
  def from_euler(cls, seq: str, angles: jax.Array, degrees: bool = False):
    """Initialize from Euler angles."""
    num_axes = len(seq)
    if num_axes < 1 or num_axes > 3:
      raise ValueError("Expected axis specification to be a non-empty "
                       "string of upto 3 characters, got {}".format(seq))
    intrinsic = (re.match(r'^[XYZ]{1,3}$', seq) is not None)
    extrinsic = (re.match(r'^[xyz]{1,3}$', seq) is not None)
    if not (intrinsic or extrinsic):
      raise ValueError("Expected axes from `seq` to be from ['x', 'y', "
                       "'z'] or ['X', 'Y', 'Z'], got {}".format(seq))
    if any(seq[i] == seq[i+1] for i in range(num_axes - 1)):
      raise ValueError("Expected consecutive axes to be different, "
                       "got {}".format(seq))
    angles = jnp.atleast_1d(angles)
    axes = jnp.array([_elementary_basis_index(x) for x in seq.lower()])
    return cls(_elementary_quat_compose(angles, axes, intrinsic, degrees))
