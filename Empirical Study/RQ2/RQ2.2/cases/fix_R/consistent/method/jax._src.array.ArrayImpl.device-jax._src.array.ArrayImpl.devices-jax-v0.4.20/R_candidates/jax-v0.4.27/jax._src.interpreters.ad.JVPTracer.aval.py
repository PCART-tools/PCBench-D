  @property
  def aval(self):
    # TODO(dougalm): add epsilon ball
    return get_aval(self.primal)
