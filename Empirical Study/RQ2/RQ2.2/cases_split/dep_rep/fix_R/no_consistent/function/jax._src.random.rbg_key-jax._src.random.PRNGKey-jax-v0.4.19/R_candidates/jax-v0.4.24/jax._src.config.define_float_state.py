def define_float_state(
    name: str,
    default: float | None,
    help: str,
    *,
    update_global_hook: Callable[[str], None] | None = None,
    update_thread_local_hook: Callable[[str | None], None] | None = None,
) -> _StateContextManager[float]:
  """Set up thread-local state and return a contextmanager for managing it.

  See docstring for ``define_bool_state``.

  Args:
    name: string, converted to lowercase to define the name of the config
      option (and absl flag). It is converted to uppercase to define the
      corresponding shell environment variable.
    default: optional float, default value.
    help: string, used to populate the flag help information as well as the
      docstring of the returned context manager.

  Returns:
    A contextmanager to control the thread-local state value.
  """
  name = name.lower()
  default_env = os.getenv(name.upper(), default)
  if default_env is not None:
    try:
      default = float(default_env)
    except ValueError:
      raise ValueError(f"Invalid value \"{default_env}\" for JAX flag {name}")
  DEFINE_float(name, default, help=help, update_hook=update_global_hook)
  config._contextmanager_flags.add(name)

  def validate(new_val):
    if new_val is not None and not isinstance(new_val, (float, int)):
      raise ValueError(
        f'new float config value must be None or of type float, '
        f'got {new_val} of type {type(new_val)}')

  s = _StateContextManager[float](name, help, update_thread_local_hook,
                                  validate)
  setattr(Config, name, property(lambda _: s.value))
  return s
