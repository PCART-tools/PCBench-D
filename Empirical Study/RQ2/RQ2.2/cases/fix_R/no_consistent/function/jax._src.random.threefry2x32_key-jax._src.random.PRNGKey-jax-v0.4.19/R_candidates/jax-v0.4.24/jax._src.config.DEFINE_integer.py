def DEFINE_integer(name, default, *args, **kwargs) -> FlagHolder[int]:
  update_hook = kwargs.pop("update_hook", None)
  config.add_option(name, default, int, args, kwargs, update_hook=update_hook)
  return FlagHolder(name)
