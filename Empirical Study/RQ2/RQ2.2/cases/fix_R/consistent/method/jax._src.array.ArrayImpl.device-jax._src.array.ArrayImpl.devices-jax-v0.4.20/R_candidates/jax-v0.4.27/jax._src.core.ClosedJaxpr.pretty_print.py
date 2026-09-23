  def pretty_print(self, *, source_info=False, print_shapes=True,
                   name_stack=False, custom_pp_eqn_rules=True,
                   print_effects=False, **kwargs):
    return self.jaxpr.pretty_print(
        source_info=source_info,
        print_shapes=print_shapes,
        name_stack=name_stack,
        custom_pp_eqn_rules=custom_pp_eqn_rules,
        print_effects=print_effects,
        **kwargs)
