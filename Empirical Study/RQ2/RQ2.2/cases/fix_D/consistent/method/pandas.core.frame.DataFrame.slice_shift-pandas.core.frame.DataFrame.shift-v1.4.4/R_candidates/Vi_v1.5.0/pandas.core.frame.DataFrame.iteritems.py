    @Appender(_shared_docs["iteritems"])
    def iteritems(self) -> Iterable[tuple[Hashable, Series]]:
        warnings.warn(
            "iteritems is deprecated and will be removed in a future version. "
            "Use .items instead.",
            FutureWarning,
            stacklevel=find_stack_level(inspect.currentframe()),
        )
        yield from self.items()
