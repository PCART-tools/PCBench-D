  def get_referent(self):
    if self.batch_dim is None or type(self.batch_dim) is int:
      return core.get_referent(self.val)
    else:  # TODO(mattjj): could handle the RaggedAxis case?
      return self
