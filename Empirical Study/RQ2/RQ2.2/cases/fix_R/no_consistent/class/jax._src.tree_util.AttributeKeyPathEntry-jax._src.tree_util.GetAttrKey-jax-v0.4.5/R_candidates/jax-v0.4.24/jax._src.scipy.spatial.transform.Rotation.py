@implements(scipy.spatial.transform.Rotation)
class Rotation(typing.NamedTuple):
  """Rotation in 3 dimensions."""

  quat: jax.Array

  @classmethod
  def concatenate(cls, rotations: typing.Sequence):
    """Concatenate a sequence of `Rotation` objects."""
    return cls(jnp.concatenate([rotation.quat for rotation in rotations]))

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

  @classmethod
  def from_matrix(cls, matrix: jax.Array):
    """Initialize from rotation matrix."""
    return cls(_from_matrix(matrix))

  @classmethod
  def from_mrp(cls, mrp: jax.Array):
    """Initialize from Modified Rodrigues Parameters (MRPs)."""
    return cls(_from_mrp(mrp))

  @classmethod
  def from_quat(cls, quat: jax.Array):
    """Initialize from quaternions."""
    return cls(_normalize_quaternion(quat))

  @classmethod
  def from_rotvec(cls, rotvec: jax.Array, degrees: bool = False):
    """Initialize from rotation vectors."""
    return cls(_from_rotvec(rotvec, degrees))

  @classmethod
  def identity(cls, num: int | None = None, dtype=float):
    """Get identity rotation(s)."""
    assert num is None
    quat = jnp.array([0., 0., 0., 1.], dtype=dtype)
    return cls(quat)

  @classmethod
  def random(cls, random_key: jax.Array, num: int | None = None):
    """Generate uniformly distributed rotations."""
    # Need to implement scipy.stats.special_ortho_group for this to work...
    raise NotImplementedError

  def __getitem__(self, indexer):
    """Extract rotation(s) at given index(es) from object."""
    if self.single:
      raise TypeError("Single rotation is not subscriptable.")
    return Rotation(self.quat[indexer])

  def __len__(self):
    """Number of rotations contained in this object."""
    if self.single:
      raise TypeError('Single rotation has no len().')
    else:
      return self.quat.shape[0]

  def __mul__(self, other):
    """Compose this rotation with the other."""
    return Rotation.from_quat(_compose_quat(self.quat, other.quat))

  def apply(self, vectors: jax.Array, inverse: bool = False) -> jax.Array:
    """Apply this rotation to one or more vectors."""
    return _apply(self.as_matrix(), vectors, inverse)

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

  def as_matrix(self) -> jax.Array:
    """Represent as rotation matrix."""
    return _as_matrix(self.quat)

  def as_mrp(self) -> jax.Array:
    """Represent as Modified Rodrigues Parameters (MRPs)."""
    return _as_mrp(self.quat)

  def as_rotvec(self, degrees: bool = False) -> jax.Array:
    """Represent as rotation vectors."""
    return _as_rotvec(self.quat, degrees)

  def as_quat(self) -> jax.Array:
    """Represent as quaternions."""
    return self.quat

  def inv(self):
    """Invert this rotation."""
    return Rotation(_inv(self.quat))

  def magnitude(self) -> jax.Array:
    """Get the magnitude(s) of the rotation(s)."""
    return _magnitude(self.quat)

  def mean(self, weights: jax.Array | None = None):
    """Get the mean of the rotations."""
    w = jnp.ones(self.quat.shape[0], dtype=self.quat.dtype) if weights is None else jnp.asarray(weights, dtype=self.quat.dtype)
    if w.ndim != 1:
      raise ValueError("Expected `weights` to be 1 dimensional, got "
                       "shape {}.".format(w.shape))
    if w.shape[0] != len(self):
      raise ValueError("Expected `weights` to have number of values "
                       "equal to number of rotations, got "
                       "{} values and {} rotations.".format(w.shape[0], len(self)))
    K = jnp.dot(w[jnp.newaxis, :] * self.quat.T, self.quat)
    _, v = jnp.linalg.eigh(K)
    return Rotation(v[:, -1])

  @property
  def single(self) -> bool:
    """Whether this instance represents a single rotation."""
    return self.quat.ndim == 1
