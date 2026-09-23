@dataclasses.dataclass(frozen=True)
class AbstractSemaphore(jax_core.AbstractValue):
  sem_type: SemaphoreType

  def join(self, other):
    if not isinstance(other, AbstractSemaphore):
      raise ValueError
    if other.sem_type != self.sem_type:
      raise ValueError
    return self
