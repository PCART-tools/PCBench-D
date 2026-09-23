class PjitInfo(NamedTuple):
  fun: Callable
  in_shardings: Any
  out_shardings: Any
  static_argnums: tuple[int, ...]
  static_argnames: tuple[str, ...]
  donate_argnums: tuple[int, ...]
  donate_argnames: tuple[str, ...]
  device: xc.Device | None
  backend: str | None
  keep_unused: bool
  inline: bool
  resource_env: Any
  abstracted_axes: Any | None
  in_layouts: Any  # pytree[XlaCompatibleLayout] | None
  out_layouts: Any  # pytree[XlaCompatibleLayout] | None
