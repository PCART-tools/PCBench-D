  def __dlpack__(self):
    from jax.dlpack import to_dlpack  # pylint: disable=g-import-not-at-top
    return to_dlpack(self)
