def register_keypaths(ty: Type, handler: Callable[[Any], List[KeyPathEntry]]
                      ) -> None:
  _keypath_registry[ty] = handler
