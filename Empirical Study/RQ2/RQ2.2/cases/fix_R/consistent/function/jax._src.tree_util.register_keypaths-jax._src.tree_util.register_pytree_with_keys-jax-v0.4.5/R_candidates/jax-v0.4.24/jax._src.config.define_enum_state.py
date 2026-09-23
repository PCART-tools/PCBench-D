def define_enum_state(
    name: str,
    enum_values: list[str],
    default: str | None,
    help: str,
    *,
    update_global_hook: Callable[[str], None] | None = None,
    update_thread_local_hook: Callable[[str | None], None] | None = None,
) -> _StateContextManager[str]:
  """Set up thread-local state and return a contextmanager for managing it.

  See docstring for ``define_bool_state``.

  Args:
    name: string, converted to lowercase to define the name of the config
      option (and absl flag). It is converted to uppercase to define the
      corresponding shell environment variable.
    enum_values: list of strings representing the possible values for the
      option.
    default: optional string, default value.
    help: string, used to populate the flag help information as well as the
      docstring of the returned context manager.

  Returns:
    A contextmanager to control the thread-local state value.
  """
  name = name.lower()
  default = os.getenv(name.upper(), default)
  if default is not None and default not in enum_values:
    raise ValueError(f"Invalid value \"{default}\" for JAX flag {name}")
  DEFINE_enum(name, default,
              enum_values=enum_values, help=help,
              update_hook=update_global_hook)
  config._contextmanager_flags.add(name)

  def validate(new_val):
    if (new_val is not None and
      (type(new_val) is not str or new_val not in enum_values)):
      raise ValueError(f"new enum value must be None or in {enum_values}, "
                       f"got {new_val} of type {type(new_val)}.")

  s = _StateContextManager[str](name, help, update_thread_local_hook, validate)
  setattr(Config, name, property(lambda _: s.value))
  return s
