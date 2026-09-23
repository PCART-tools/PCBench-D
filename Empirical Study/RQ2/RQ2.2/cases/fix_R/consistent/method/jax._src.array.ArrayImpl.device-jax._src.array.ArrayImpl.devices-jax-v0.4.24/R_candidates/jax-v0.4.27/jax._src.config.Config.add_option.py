  def add_option(self, name, holder, opt_type, meta_args, meta_kwargs):
    if name in self._value_holders:
      raise Exception(f"Config option {name} already defined")
    self._value_holders[name] = holder
    self.meta[name] = (opt_type, meta_args, meta_kwargs)
