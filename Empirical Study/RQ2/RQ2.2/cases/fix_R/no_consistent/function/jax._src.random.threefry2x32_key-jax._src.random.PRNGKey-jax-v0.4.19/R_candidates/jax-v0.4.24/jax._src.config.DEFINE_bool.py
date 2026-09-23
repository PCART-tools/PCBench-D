def DEFINE_bool(name, default, *args, **kwargs) -> FlagHolder[bool]:
  update_hook = kwargs.pop("update_hook", None)
  config.add_option(name, default, bool, args, kwargs, update_hook=update_hook)
  return FlagHolder(name)
