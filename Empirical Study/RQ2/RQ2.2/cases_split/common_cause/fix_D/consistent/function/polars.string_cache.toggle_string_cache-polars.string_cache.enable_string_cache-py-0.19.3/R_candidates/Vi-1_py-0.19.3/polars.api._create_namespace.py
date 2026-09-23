def _create_namespace(
    name: str, cls: type[Expr | DataFrame | LazyFrame | Series]
) -> Callable[[type[NS]], type[NS]]:
    """Register custom namespace against the underlying polars class."""

    def namespace(ns_class: type[NS]) -> type[NS]:
        if name in _reserved_namespaces:
            raise AttributeError(f"cannot override reserved namespace {name!r}")
        elif hasattr(cls, name):
            warn(
                f"Overriding existing custom namespace {name!r} (on {cls.__name__!r})",
                UserWarning,
                stacklevel=find_stacklevel(),
            )

        setattr(cls, name, NameSpace(name, ns_class))
        cls._accessors.add(name)
        return ns_class

    return namespace
