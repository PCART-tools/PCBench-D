  def strip_weak_type(self):
    """Returns a copy of the aval with weak_type=False."""
    return self.update(weak_type=False)
