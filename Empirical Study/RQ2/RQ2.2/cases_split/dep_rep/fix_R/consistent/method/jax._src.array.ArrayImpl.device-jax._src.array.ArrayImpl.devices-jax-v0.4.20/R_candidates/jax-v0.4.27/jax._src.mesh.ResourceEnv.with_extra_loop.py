  def with_extra_loop(self, loop: Loop):
    if loop.name in self.resource_axes:
      raise ValueError(f"Cannot extend the resource environment with loop named "
                       f"`{loop.name}`. An axis of this name is already defined!")
    return self._replace(loops=self.loops + (loop,))
