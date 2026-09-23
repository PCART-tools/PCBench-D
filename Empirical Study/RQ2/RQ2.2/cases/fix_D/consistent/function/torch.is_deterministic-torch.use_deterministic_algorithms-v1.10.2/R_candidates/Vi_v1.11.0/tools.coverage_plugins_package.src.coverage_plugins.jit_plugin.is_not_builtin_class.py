def is_not_builtin_class(obj: Any) -> bool:
    return isclass(obj) and not type(obj).__module__ == 'builtins'
