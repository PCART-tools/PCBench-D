  def _pretty_print(self, context: core.JaxprPpContext) -> pp.Doc:
    if isinstance(self.input_index, core.Var):
      index_text = pp.text(core.pp_var(self.input_index, context))
    else:
      index_text = pp.text(self.input_index)
    return pp.concat([
      pp.color(pp.text(self.name), foreground=_ref_effect_color),
      pp.text("<"),
      index_text,
      pp.text(">")])
