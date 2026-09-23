  @classmethod
  def identity(cls, num: int | None = None, dtype=float):
    """Get identity rotation(s)."""
    assert num is None
    quat = jnp.array([0., 0., 0., 1.], dtype=dtype)
    return cls(quat)
