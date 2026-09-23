  def join(self, other):
    if not isinstance(other, AbstractSemaphore):
      raise ValueError
    if other.sem_type != self.sem_type:
      raise ValueError
    return self
