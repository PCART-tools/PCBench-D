  def __str__(self):
    if self.name == 'IN_SHARDING':
      return 'explicit input sharding'
    elif self.name == 'OUT_SHARDING':
      return 'explicit output sharding'
    elif self.name == 'CONTEXT_DEVICES':
      return 'devices'
    return f'{self.name}'
