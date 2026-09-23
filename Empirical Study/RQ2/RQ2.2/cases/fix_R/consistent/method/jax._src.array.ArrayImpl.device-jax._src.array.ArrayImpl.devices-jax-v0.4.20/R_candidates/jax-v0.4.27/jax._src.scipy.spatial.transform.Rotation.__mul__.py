  def __mul__(self, other):
    """Compose this rotation with the other."""
    return Rotation.from_quat(_compose_quat(self.quat, other.quat))
