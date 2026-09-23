@bint_p.def_abstract_eval
def bint_abstract_eval(_, *, bd: int):
  return core.AbstractBInt(bound=bd)
