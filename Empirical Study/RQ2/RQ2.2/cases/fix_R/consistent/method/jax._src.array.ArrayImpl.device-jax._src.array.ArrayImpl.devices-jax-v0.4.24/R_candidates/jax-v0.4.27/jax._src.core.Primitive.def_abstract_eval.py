  def def_abstract_eval(self, abstract_eval):
    self.abstract_eval = _effect_free_abstract_eval(abstract_eval)  # type: ignore[assignment]
    return abstract_eval
