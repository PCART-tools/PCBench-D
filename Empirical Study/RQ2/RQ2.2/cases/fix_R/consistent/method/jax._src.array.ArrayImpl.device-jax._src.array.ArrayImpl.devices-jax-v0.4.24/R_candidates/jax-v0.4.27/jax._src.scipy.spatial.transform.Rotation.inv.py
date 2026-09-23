  def inv(self):
    """Invert this rotation."""
    return Rotation(_inv(self.quat))
