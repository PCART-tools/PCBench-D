  def def_effectful_abstract_eval(self, effectful_abstract_eval):
    self.abstract_eval = effectful_abstract_eval  # type: ignore[assignment]
    return effectful_abstract_eval
