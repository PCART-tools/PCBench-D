def define_bool_state(
    name: str,
    default: bool,
    help: str,
    *,
    update_global_hook: Callable[[bool], None] | None = None,
    update_thread_local_hook: Callable[[bool | None], None] | None = None,
    upgrade: bool = False,
    extra_description: str = '',
) -> _StateContextManager[bool]:
  """Set up thread-local state and return a contextmanager for managing it.

  This function is a convenience wrapper. It defines a flag, environment
  variable, and corresponding thread-local state, which can be managed via the
  contextmanager it returns.

  The thread-local state value can be read via the ``config.<option_name>``
  attribute, where ``config`` is the singleton ``Config`` instance.

  Args:
    name: string, converted to lowercase to define the name of the config
      option (and absl flag). It is converted to uppercase to define the
      corresponding shell environment variable.
    default: boolean, a default value for the option.
    help: string, used to populate the flag help information as well as the
      docstring of the returned context manager.
    update_global_hook: a optional callback that is called with the updated
      value of the global state when it is altered or set initially.
    update_thread_local_hook: a optional callback that is called with the
      updated value of the thread-local state when it is altered or set
      initially.
    upgrade: optional indicator that this flag controls a canonical feature
      upgrade, so that it is `True` for the incoming functionality, `False`
      for the outgoing functionality to be deprecated.
    extra_description: string, optional: extra information to add to the
      summary description.

  Returns:
    A contextmanager to control the thread-local state value.

  Example:

    enable_foo = config.define_bool_state(
        name='jax_enable_foo',
        default=False,
        help='Enable foo.')

    # Now the JAX_ENABLE_FOO shell environment variable and --jax_enable_foo
    # command-line flag can be used to control the process-level value of
    # the configuration option, in addition to using e.g.
    # ``config.update("jax_enable_foo", True)`` directly. We can also use a
    # context manager:

    with enable_foo(True):
      ...

  The value of the thread-local state or flag can be accessed via
  ``config.jax_enable_foo``. Reading it via ``config.FLAGS.jax_enable_foo`` is
  an error.
  """
  name = name.lower()
  if upgrade:
    help += ' ' + UPGRADE_BOOL_HELP
    extra_description += UPGRADE_BOOL_EXTRA_DESC
  DEFINE_bool(name, bool_env(name.upper(), default), help,
              update_hook=update_global_hook)
  config._contextmanager_flags.add(name)

  s = _StateContextManager[bool](
      name, help, update_thread_local_hook,
      extra_description=extra_description, default_value=True)
  setattr(Config, name, property(lambda _: s.value))
  return s
