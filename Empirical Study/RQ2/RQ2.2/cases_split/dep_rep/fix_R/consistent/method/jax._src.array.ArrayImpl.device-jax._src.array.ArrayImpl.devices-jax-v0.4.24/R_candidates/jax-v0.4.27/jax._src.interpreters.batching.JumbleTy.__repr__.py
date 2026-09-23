  def __repr__(self) -> str:
    return f'Var{id(self.binder)}:{self.length} => {self.elt_ty}'
