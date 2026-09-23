def is_vmappable(x: Any) -> bool:
  return type(x) is Pile or type(x) in vmappables
