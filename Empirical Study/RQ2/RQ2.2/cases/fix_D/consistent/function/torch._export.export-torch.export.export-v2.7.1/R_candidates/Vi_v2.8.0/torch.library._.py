    @impl.register
    def _(
        lib: Library, name: str, dispatch_key: str = ""
    ) -> Callable[[Callable[_P, _T]], Callable[_P, _T]]:
        """Legacy torch.library.impl API. Kept around for BC"""

        def wrap(f: Callable[_P, _T]) -> Callable[_P, _T]:
            lib.impl(name, f, dispatch_key)
            return f

        return wrap
