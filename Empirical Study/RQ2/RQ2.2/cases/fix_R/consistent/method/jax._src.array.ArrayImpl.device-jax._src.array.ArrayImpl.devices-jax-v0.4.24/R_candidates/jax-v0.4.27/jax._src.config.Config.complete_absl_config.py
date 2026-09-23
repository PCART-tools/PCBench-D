  def complete_absl_config(self, absl_flags):
    # NOTE: avoid calling from outside this module. Instead, use
    # `config_with_absl()`, and (in rare cases) `parse_flags_with_absl()`.
    for name, holder in self._value_holders.items():
      try:
        flag = absl_flags.FLAGS[name]
      except KeyError:
        # This can happen if a new flag was added after config_with_absl() was
        # called, but before complete_absl_config was run. We could in principle
        # add code to DEFINE_... to register any newly added flags with ABSL
        # if config_with_absl() has already been called, but arguably the user
        # should have called config_with_absl() later.
        continue
      if flag.present:
        holder._set(flag.value)
