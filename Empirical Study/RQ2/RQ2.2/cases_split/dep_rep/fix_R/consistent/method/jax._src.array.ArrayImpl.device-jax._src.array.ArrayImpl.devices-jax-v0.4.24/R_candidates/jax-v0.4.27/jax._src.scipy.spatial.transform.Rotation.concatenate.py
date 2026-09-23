  @classmethod
  def concatenate(cls, rotations: typing.Sequence):
    """Concatenate a sequence of `Rotation` objects."""
    return cls(jnp.concatenate([rotation.quat for rotation in rotations]))
