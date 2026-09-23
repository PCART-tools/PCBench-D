def register_keypaths(ty: Type, handler: Callable[[Any], Sequence[KeyPathEntry]]
                      ) -> None:
  _keypath_registry[ty] = handler
