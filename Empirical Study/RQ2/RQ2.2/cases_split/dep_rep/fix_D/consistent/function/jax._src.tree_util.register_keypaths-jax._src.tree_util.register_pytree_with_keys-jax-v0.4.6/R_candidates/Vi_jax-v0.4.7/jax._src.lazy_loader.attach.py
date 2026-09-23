def attach(package_name: str, submodules: Sequence[str]) -> Tuple[
    Callable[[str], Any],
    Callable[[], List[str]],
    List[str],
]:
  """Lazily loads submodules of a package.

  Example use:
  ```
  __getattr__, __dir__, __all__ = lazy_loader.attach(__name__, ["sub1", "sub2"])
  ```
  """

  __all__: List[str] = list(submodules)

  def __getattr__(name: str) -> Any:
    if name in submodules:
      return importlib.import_module(f"{package_name}.{name}")
    raise AttributeError(f"module '{package_name}' has no attribute '{name}")

  def __dir__() -> List[str]:
    return __all__

  return __getattr__, __dir__, __all__
