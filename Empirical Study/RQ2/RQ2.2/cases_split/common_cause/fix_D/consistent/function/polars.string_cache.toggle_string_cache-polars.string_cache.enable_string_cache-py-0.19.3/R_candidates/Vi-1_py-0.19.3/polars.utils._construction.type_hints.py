    def type_hints(obj: type) -> dict[str, Any]:
        try:
            # often the same as obj.__annotations__, but handles forward references
            # encoded as string literals, adds Optional[t] if a default value equal
            # to None is set and recursively replaces 'Annotated[T, ...]' with 'T'.
            return get_type_hints(obj)
        except TypeError:
            # fallback on edge-cases (eg: InitVar inference on python 3.10).
            return _get_annotations(obj)
