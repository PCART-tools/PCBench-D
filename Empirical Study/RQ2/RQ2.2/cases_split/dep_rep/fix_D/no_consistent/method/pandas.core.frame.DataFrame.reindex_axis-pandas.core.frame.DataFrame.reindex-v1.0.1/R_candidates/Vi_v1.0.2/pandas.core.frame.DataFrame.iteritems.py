    @Appender(_shared_docs["items"])
    def iteritems(self) -> Iterable[Tuple[Optional[Hashable], Series]]:
        yield from self.items()
