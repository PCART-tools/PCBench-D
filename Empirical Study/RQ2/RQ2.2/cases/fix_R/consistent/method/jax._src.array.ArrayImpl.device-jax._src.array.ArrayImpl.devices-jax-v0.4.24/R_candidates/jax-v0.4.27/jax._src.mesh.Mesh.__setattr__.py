  def __setattr__(self, name, value):
    if hasattr(self, name):
      if getattr(self, name) == value:
        # This can to happen if two threads race, for example if two threads
        # are trying to hash the same Mesh instance.
        return
      raise RuntimeError(
          f"Cannot reassign attributes ({name}) of immutable mesh objects"
      )
    super().__setattr__(name, value)
