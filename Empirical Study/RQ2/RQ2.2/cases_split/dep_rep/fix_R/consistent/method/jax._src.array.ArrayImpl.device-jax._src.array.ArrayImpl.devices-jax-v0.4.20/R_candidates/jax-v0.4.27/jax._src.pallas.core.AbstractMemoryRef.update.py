  def update(self, inner_aval=None, memory_space=None):
    inner_aval = self.inner_aval if inner_aval is None else inner_aval
    memory_space = self.memory_space if memory_space is None else memory_space
    return AbstractMemoryRef(inner_aval, memory_space)
