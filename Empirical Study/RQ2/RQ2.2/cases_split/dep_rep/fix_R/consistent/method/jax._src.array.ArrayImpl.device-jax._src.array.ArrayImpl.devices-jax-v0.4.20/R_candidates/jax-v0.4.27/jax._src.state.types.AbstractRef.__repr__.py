  def __repr__(self) -> str:
    return f'Ref{{{self.inner_aval.str_short()}}}'
