def is_vmappable(x: Any) -> bool:
  return type(x) is Jumble or type(x) in vmappables
