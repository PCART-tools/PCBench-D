def DEFINE_string(name, default, *args, **kwargs) -> FlagHolder[str]:
  update_hook = kwargs.pop("update_hook", None)
  config.add_option(name, default, str, args, kwargs, update_hook=update_hook)
  return FlagHolder(name)
