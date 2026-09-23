class Config:
  _HAS_DYNAMIC_ATTRIBUTES = True

  def __init__(self):
    self.values = {}
    self.meta = {}
    self.use_absl = False
    self._contextmanager_flags = set()
    self._update_hooks = {}

  def __getattr__(self, name):
    fn = None
    if name in _CONFIG_DEPRECATIONS:
      fn = globals().get(name, None)
    if fn is None:
      raise AttributeError(
          f"'{type(self).__name__!r} object has no attribute {name!r}")
    message = (
        f"jax.config.{name} is deprecated. Please use other libraries "
        "for configuration instead."
    )
    warnings.warn(message, DeprecationWarning, stacklevel=2)
    return fn

  def update(self, name, val):
    if name not in self.values:
      raise AttributeError(f"Unrecognized config option: {name}")
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
    try:
      return self.values[name]
    except KeyError:
      raise AttributeError(f"Unrecognized config option: {name}")

  def add_option(self, name, default, opt_type, meta_args, meta_kwargs,
                 update_hook: Callable[[Any], None] | None = None):
    if name in self.values:
      raise Exception(f"Config option {name} already defined")
    self.values[name] = default
    self.meta[name] = (opt_type, meta_args, meta_kwargs)
    if update_hook:
      self._update_hooks[name] = update_hook
      update_hook(default)

  def config_with_absl(self):
    """Registers absl flags for the JAX configs.

    E.g., for each JAX config defined using define_bool_state(), this method
    registers an absl boolean flag, with the same name.

    This is the recommended method to call if you use `app.run(main)` and you
    need JAX flags.  Example:

    ```python
    from absl import app
    import jax
    ...

    if __name__ == '__main__':
      jax.config.config_with_absl()
      app.run(main)
    ```

    """
    import absl.flags as absl_FLAGS  # noqa: F401  # pytype: disable=import-error
    from absl import app, flags as absl_flags  # pytype: disable=import-error

    self.use_absl = True
    self.absl_flags = absl_flags
    absl_defs = { bool: absl_flags.DEFINE_bool,
                  int:  absl_flags.DEFINE_integer,
                  float: absl_flags.DEFINE_float,
                  str:  absl_flags.DEFINE_string,
                  'enum': absl_flags.DEFINE_enum }

    for name, val in self.values.items():
      flag_type, meta_args, meta_kwargs = self.meta[name]
      absl_defs[flag_type](name, val, *meta_args, **meta_kwargs)
    app.call_after_init(lambda: self.complete_absl_config(absl_flags))

  def complete_absl_config(self, absl_flags):
    # NOTE: avoid calling from outside this module. Instead, use
    # `config_with_absl()`, and (in rare cases) `parse_flags_with_absl()`.
    for name, _ in self.values.items():
      try:
        flag = absl_flags.FLAGS[name]
      except KeyError:
        # This can happen if a new flag was added after config_with_absl() was
        # called, but before complete_absl_config was run. We could in principle
        # add code to DEFINE_... to register any newly added flags with ABSL
        # if config_with_absl() has already been called, but arguably the user
        # should have called config_with_absl() later.
        continue
      if flag.present:
        self.update(name, flag.value)

  def parse_flags_with_absl(self):
    """Parses command-line args that start with --jax.

    This method should be used only by advanced users. Most users should use
    :meth:`config_with_absl` instead.

    This method has serious limitations: e.g., although it parses only the
    --jax* command-line args, it runs the validators of all registered absl
    flags, even non-JAX ones that have not been set yet; as such, for the
    non-JAX flags, the validators run on the default flag values, not on the
    values indicated by the command-line args.
    """
    global already_configured_with_absl
    if not already_configured_with_absl:
      # Extract just the --jax... flags (before the first --) from argv. In some
      # environments (e.g. ipython/colab) argv might be a mess of things
      # parseable by absl and other junk.
      jax_argv = itertools.takewhile(lambda a: a != '--', sys.argv)
      jax_argv = ['', *(a for a in jax_argv if a.startswith('--jax'))]

      import absl.flags  # pytype: disable=import-error
      self.config_with_absl()
      absl.flags.FLAGS(jax_argv, known_only=True)
      self.complete_absl_config(absl.flags)
      already_configured_with_absl = True

  def _trace_context(self):
    """Returns a tuple of configuration values that affect tracing.

    These values are included in the cache key for linear_util.cache.

    Values included in this set should also most likely be included in
    the C++ JIT state, which is handled separately.
    """
    tls = jax_jit.thread_local_state()
    axis_env_state = ()
    mesh_context_manager = ()
    context = tls.extra_jit_context
    if context and context.axis_env_state is not None:
      axis_env_state = context.axis_env_state
    if context and context.mesh_context_manager:
      mesh_context_manager = context.mesh_context_manager
    return (axis_env_state, mesh_context_manager, self.x64_enabled,
            self.jax_numpy_rank_promotion, self.jax_default_matmul_precision,
            self.jax_dynamic_shapes, self.jax_numpy_dtype_promotion,
            self.jax_default_device,
            self.jax_random_seed_offset,
            self.jax_threefry_partitionable,
            self.jax_softmax_custom_jvp,
            self.jax_enable_memories,
            self.jax_disable_jit,
            self.jax_xla_profile_version,
            # Technically this affects jaxpr->stablehlo lowering, not tracing.
            self.jax_hlo_source_file_canonicalization_regex)
