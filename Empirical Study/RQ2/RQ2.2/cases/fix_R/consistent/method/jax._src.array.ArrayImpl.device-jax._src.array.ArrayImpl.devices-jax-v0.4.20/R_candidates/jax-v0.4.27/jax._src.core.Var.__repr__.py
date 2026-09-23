  def __repr__(self):
    return f'Var(id={id(self)}){self.suffix}:{self.aval.str_short()}'
