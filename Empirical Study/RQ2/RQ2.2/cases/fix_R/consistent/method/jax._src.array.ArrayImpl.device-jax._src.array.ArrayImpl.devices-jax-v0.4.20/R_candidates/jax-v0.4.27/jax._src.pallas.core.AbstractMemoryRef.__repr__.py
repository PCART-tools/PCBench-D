  def __repr__(self) -> str:
    return f'MemRef<{self.memory_space}>{{{self.inner_aval.str_short()}}}'
