  def __init__(
      self,
      name: str,
      default: _T,
      help,
      update_global_hook: Callable[[_T], None] | None = None,
      update_thread_local_hook: Callable[[_T | None], None] | None = None,
      validator: Callable[[Any], None] | None = None,
      extra_description: str = '',
      default_context_manager_value: Any = no_default,
  ):
    self._name = name
    self.__name__ = name[4:] if name.startswith('jax_') else name
    self.__doc__ = (f"Context manager for `{name}` config option"
                    f"{extra_description}.\n\n{help}")
    self._update_global_hook = update_global_hook
    self._update_thread_local_hook = update_thread_local_hook
    self._validator = validator
    self._default_context_manager_value = default_context_manager_value
    self._set(default)
