    @Appender(_shared_docs["items"])
    def iteritems(self) -> Iterable[tuple[Hashable, Series]]:
        yield from self.items()
