class MismatchType(enum.Enum):
  ARG_SHARDING = 0
  OUT_SHARDING = 1
  SHARDING_INSIDE_COMPUTATION = 2
  CONTEXT_DEVICES = 3
  IN_SHARDING = 4

  def __str__(self):
    if self.name == 'IN_SHARDING':
      return 'explicit input sharding'
    elif self.name == 'OUT_SHARDING':
      return 'explicit output sharding'
    elif self.name == 'CONTEXT_DEVICES':
      return 'devices'
    return f'{self.name}'
