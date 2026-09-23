class Config:
  _HAS_DYNAMIC_ATTRIBUTES = True

  def __init__(self):
    self.values = {}
    self.meta = {}
    self.FLAGS = NameSpace(self.read, self.update)
    self.use_absl = False
    self._contextmanager_flags = set()
    self._update_hooks = {}

  def update(self, name, val):
    if self.use_absl:
      setattr(self.absl_flags.FLAGS, name, val)
    else:
      self.check_exists(name)
      if name not in self.values:
        raise Exception(f"Unrecognized config option: {name}")
      self.values[name] = val

    hook = self._update_hooks.get(name, None)
    if hook:
      hook(val)

  def read(self, name):
    if name in self._contextmanager_flags:
      raise AttributeError(
          "For flags with a corresponding contextmanager, read their value "
          f"via e.g. `config.{name}` rather than `config.FLAGS.{name}`.")
    return self._read(name)

  def _read(self, name):
    if self.use_absl:
      return getattr(self.absl_flags.FLAGS, name)
    else:
      self.check_exists(name)
      return self.values[name]

  def add_option(self, name, default, opt_type, meta_args, meta_kwargs,
                 update_hook=None):
    if name in self.values:
      raise Exception(f"Config option {name} already defined")
    self.values[name] = default
    self.meta[name] = (opt_type, meta_args, meta_kwargs)
    if update_hook:
      self._update_hooks[name] = update_hook
      update_hook(default)

  def check_exists(self, name):
    if name not in self.values:
      raise AttributeError(f"Unrecognized config option: {name}")

  def DEFINE_bool(self, name, default, *args, **kwargs):
    update_hook = kwargs.pop("update_hook", None)
    self.add_option(name, default, bool, args, kwargs, update_hook=update_hook)

  def DEFINE_integer(self, name, default, *args, **kwargs):
    update_hook = kwargs.pop("update_hook", None)
    self.add_option(name, default, int, args, kwargs, update_hook=update_hook)

  def DEFINE_string(self, name, default, *args, **kwargs):
    update_hook = kwargs.pop("update_hook", None)
    self.add_option(name, default, str, args, kwargs, update_hook=update_hook)

  def DEFINE_enum(self, name, default, *args, **kwargs):
    update_hook = kwargs.pop("update_hook", None)
    self.add_option(name, default, 'enum', args, kwargs,
                    update_hook=update_hook)

  def config_with_absl(self):
    # Run this before calling `app.run(main)` etc
    import absl.flags as absl_FLAGS  # noqa: F401
    from absl import app, flags as absl_flags

    self.use_absl = True
    self.absl_flags = absl_flags
    absl_defs = { bool: absl_flags.DEFINE_bool,
                  int:  absl_flags.DEFINE_integer,
                  str:  absl_flags.DEFINE_string,
                  'enum': absl_flags.DEFINE_enum }

    for name, val in self.values.items():
      flag_type, meta_args, meta_kwargs = self.meta[name]
      absl_defs[flag_type](name, val, *meta_args, **meta_kwargs)
    app.call_after_init(lambda: self.complete_absl_config(absl_flags))

  def complete_absl_config(self, absl_flags):
    for name, _ in self.values.items():
      self.update(name, getattr(absl_flags.FLAGS, name))

  def parse_flags_with_absl(self):
    global already_configured_with_absl
    if not already_configured_with_absl:
      # Extract just the --jax... flags (before the first --) from argv. In some
      # environments (e.g. ipython/colab) argv might be a mess of things
      # parseable by absl and other junk.
      jax_argv = itertools.takewhile(lambda a: a != '--', sys.argv)
      jax_argv = ['', *(a for a in jax_argv if a.startswith('--jax'))]

      import absl.flags
      self.config_with_absl()
      absl.flags.FLAGS(jax_argv, known_only=True)
      self.complete_absl_config(absl.flags)
      already_configured_with_absl = True

  def define_bool_state(
    self, name: str, default: bool, help: str, *,
    update_global_hook: Optional[Callable[[bool], None]] = None,
    update_thread_local_hook: Optional[Callable[[Optional[bool]], None]] = None,
    upgrade: bool = False,
    extra_description: str = ""):
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
    self.DEFINE_bool(name, bool_env(name.upper(), default), help,
                     update_hook=update_global_hook)
    self._contextmanager_flags.add(name)

    def get_state(self):
      val = getattr(_thread_local_state, name, unset)
      return val if val is not unset else self._read(name)
    setattr(Config, name, property(get_state))

    return _StateContextManager(name, help, update_thread_local_hook,
                                extra_description=extra_description,
                                default_value=True)

  def define_enum_state(
      self, name: str, enum_values: List[str], default: Optional[str],
      help: str, update_global_hook: Optional[Callable[[str], None]] = None,
      update_thread_local_hook: Optional[Callable[[Optional[str]], None]] \
        = None):
    """Set up thread-local state and return a contextmanager for managing it.
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
    See docstring for ``define_bool_state``.
    """
    name = name.lower()
    default = os.getenv(name.upper(), default)
    if default is not None and default not in enum_values:
      raise ValueError(f"Invalid value \"{default}\" for JAX flag {name}")
    self.DEFINE_enum(name, default,
                     enum_values=enum_values, help=help,
                     update_hook=update_global_hook)
    self._contextmanager_flags.add(name)

    def get_state(self):
      val = getattr(_thread_local_state, name, unset)
      return val if val is not unset else self._read(name)
    setattr(Config, name, property(get_state))

    def validate(new_val):
      if (new_val is not None and
          (type(new_val) is not str or new_val not in enum_values)):
        raise ValueError(f"new enum value must be None or in {enum_values}, "
                         f"got {new_val} of type {type(new_val)}.")

    return _StateContextManager(name, help, update_thread_local_hook, validate)

  def define_string_state(
      self, name: str, default: Optional[str], help: str,
      update_global_hook: Optional[Callable[[str], None]] = None,
      update_thread_local_hook: Optional[Callable[[Optional[str]], None]] = None):
    """Set up thread-local state and return a contextmanager for managing it.

    See docstring for ``define_bool_state``.

    Args:
      name: string, converted to lowercase to define the name of the config
        option (and absl flag). It is converted to uppercase to define the
        corresponding shell environment variable.
      default: string, a default value for the option.
      help: string, used to populate the flag help information as well as the
        docstring of the returned context manager.
      update_global_hook: an optional callback that is called with the updated
        value of the global state when it is altered or set initially.
      update_thread_local_hook: an optional callback that is called with the
        updated value of the thread-local state when it is altered or set
        initially.

    Returns:
      A contextmanager to control the thread-local state value.
    """

    def validate(new_val):
      if new_val is not None and not isinstance(new_val, str):
        raise ValueError(f'new string config value must be None or of type str,'
                         f' got {new_val} of type {type(new_val)}.')

    return self.define_string_or_object_state(name, default, help,
                                              update_global_hook,
                                              update_thread_local_hook,
                                              validate)

  def define_string_or_object_state(
      self,
      name: str,
      default: Any,
      help: str,
      update_global_hook: Optional[Callable[[Any], None]] = None,
      update_thread_local_hook: Optional[Callable[[Any], None]] = None,
      validate_new_val_hook: Optional[Callable[[Any], None]] = None):
    """Set up thread-local state and return a contextmanager for managing it.

    Similar to ``define_string_state``, except the context manager will accept
    any object, not just a string. Any value passed via commandline flag or
    environment variable will be treated as a string.

    Args:
      name: string, converted to lowercase to define the name of the config
        option (and absl flag). It is converted to uppercase to define the
        corresponding shell environment variable.
      default: string, a default value for the option.
      help: string, used to populate the flag help information as well as the
        docstring of the returned context manager.
      update_global_hook: an optional callback that is called with the updated
        value of the global state when it is altered or set initially.
      update_thread_local_hook: an optional callback that is called with the
        updated value of the thread-local state when it is altered or set
        initially.
      validate_new_val_hook: an optional callback that is called with the new
        value on any update, and should raise an error if the new value is
        invalid.

    Returns:
      A contextmanager to control the thread-local state value.
    """
    name = name.lower()
    default = os.getenv(name.upper(), default)
    self.DEFINE_string(name, default, help=help,
                       update_hook=update_global_hook)
    self._contextmanager_flags.add(name)

    def get_state(self):
      val = getattr(_thread_local_state, name, unset)
      return val if val is not unset else self._read(name)
    setattr(Config, name, property(get_state))

    return _StateContextManager(name, help, update_thread_local_hook,
                                validate_new_val_hook)

  def _trace_context(self):
    """Returns a tuple of configuration values that affect tracing.

    These values are included in the cache key for linear_util.cache.

    Values included in this set should also most likely be included in
    the C++ JIT state, which is handled separately."""
    tls = jax_jit.thread_local_state()
    axis_env_state = ()
    context = tls.extra_jit_context
    if context and context.axis_env_state is not None:
      axis_env_state = context.axis_env_state
    return (axis_env_state, self.x64_enabled, self.jax_numpy_rank_promotion,
            self.jax_default_matmul_precision, self.jax_dynamic_shapes,
            self.jax_numpy_dtype_promotion, self.jax_default_device)
