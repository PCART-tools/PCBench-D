  def as_euler(self, seq: str, degrees: bool = False):
    """Represent as Euler angles."""
    if len(seq) != 3:
      raise ValueError(f"Expected 3 axes, got {seq}.")
    intrinsic = (re.match(r'^[XYZ]{1,3}$', seq) is not None)
    extrinsic = (re.match(r'^[xyz]{1,3}$', seq) is not None)
    if not (intrinsic or extrinsic):
      raise ValueError("Expected axes from `seq` to be from "
                       "['x', 'y', 'z'] or ['X', 'Y', 'Z'], "
                       "got {}".format(seq))
    if any(seq[i] == seq[i+1] for i in range(2)):
      raise ValueError("Expected consecutive axes to be different, "
                       "got {}".format(seq))
    axes = jnp.array([_elementary_basis_index(x) for x in seq.lower()])
    return _compute_euler_from_quat(self.quat, axes, extrinsic, degrees)
