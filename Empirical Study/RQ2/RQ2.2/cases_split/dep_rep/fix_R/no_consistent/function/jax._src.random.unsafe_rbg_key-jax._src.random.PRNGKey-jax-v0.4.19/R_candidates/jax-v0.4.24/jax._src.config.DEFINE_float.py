def DEFINE_float(name, default, *args, **kwargs) -> FlagHolder[float]:
  update_hook = kwargs.pop("update_hook", None)
  config.add_option(name, default, float, args, kwargs,
                    update_hook=update_hook)
  return FlagHolder(name)
