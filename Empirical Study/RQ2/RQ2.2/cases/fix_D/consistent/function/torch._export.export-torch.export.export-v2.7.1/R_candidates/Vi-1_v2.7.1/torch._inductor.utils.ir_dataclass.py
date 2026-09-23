@dataclass_transform(frozen_default=True)
def ir_dataclass(cls: Optional[type[Any]] = None, /, *, frozen: bool = True) -> Any:
    def wrap(cls: _T) -> _T:
        if sys.version_info >= (3, 10):
            return dataclasses.dataclass(cls, kw_only=True, frozen=frozen)  # type: ignore[call-overload]
        else:
            # Polyfill for python=3.9. kw_only simply introduces an extra check
            # that only kwargs are used (and is not available on 3.9)
            return dataclasses.dataclass(cls, frozen=frozen)

    if cls is None:
        return wrap
    return wrap(cls)
