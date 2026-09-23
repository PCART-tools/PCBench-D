  def pretty_print(self, *, source_info=False, print_shapes=True,
                   custom_pp_eqn_rules=True, name_stack=False,
                   print_effects: bool = False, **kwargs):
    doc = pp_toplevel_jaxpr(
      self, source_info=source_info, print_shapes=print_shapes,
      custom_pp_eqn_rules=custom_pp_eqn_rules, name_stack=name_stack,
      print_effects=print_effects)
    return doc.format(**kwargs)
