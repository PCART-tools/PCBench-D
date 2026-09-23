class _StateContextManager(Generic[_T]):
  def __init__(self, name, help, update_thread_local_hook,
               validate_new_val_hook: Callable[[Any], None] | None = None,
               extra_description: str = "", default_value: Any = no_default):
    self._name = name
    self.__name__ = name[4:] if name.startswith('jax_') else name
    self.__doc__ = (f"Context manager for `{name}` config option"
                    f"{extra_description}.\n\n{help}")
    self._update_thread_local_hook = update_thread_local_hook
    self._validate_new_val_hook = validate_new_val_hook
    self._default_value = default_value

  def __bool__(self) -> NoReturn:
    raise TypeError(
        "bool() not supported for instances of type '{0}' "
        "(did you mean to use '{0}.value' instead?)".format(
            type(self).__name__))

  @property
  def value(self) -> _T:
    val = _thread_local_state.__dict__.get(self._name, unset)
    return val if val is not unset else config._read(self._name)

  @contextlib.contextmanager
  def __call__(self, new_val: Any = no_default):
    if new_val is no_default:
      if self._default_value is not no_default:
        new_val = self._default_value  # default_value provided to constructor
      else:
        # no default_value provided to constructor and no value provided as an
        # argument, so we raise an error
        raise TypeError(f"Context manager for {self.__name__} config option "
                        "requires an argument representing the new value for "
                        "the config option.")
    if self._validate_new_val_hook:
      self._validate_new_val_hook(new_val)
    prev_val = getattr(_thread_local_state, self._name, unset)
    setattr(_thread_local_state, self._name, new_val)
    if self._update_thread_local_hook:
      self._update_thread_local_hook(new_val)
    try:
      yield
    finally:
      if prev_val is unset:
        delattr(_thread_local_state, self._name)
        if self._update_thread_local_hook:
          self._update_thread_local_hook(None)
      else:
        setattr(_thread_local_state, self._name, prev_val)
        if self._update_thread_local_hook:
          self._update_thread_local_hook(prev_val)

  def _add_hooks(self, update_global_hook, update_thread_local_hook):
    """Private method that adds hooks to an existing context-manager.

    Used to avoid cyclic import dependencies."""
    self._update_thread_local_hook = update_thread_local_hook
    config._update_hooks[self._name] = update_global_hook
    update_global_hook(config._read(self._name))
