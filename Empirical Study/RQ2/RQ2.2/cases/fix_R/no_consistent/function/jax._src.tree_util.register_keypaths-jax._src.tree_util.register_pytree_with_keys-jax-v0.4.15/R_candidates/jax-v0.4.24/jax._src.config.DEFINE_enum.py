def DEFINE_enum(name, default, *args, **kwargs) -> FlagHolder[str]:
  update_hook = kwargs.pop("update_hook", None)
  config.add_option(name, default, 'enum', args, kwargs,
                    update_hook=update_hook)
  return FlagHolder(name)
