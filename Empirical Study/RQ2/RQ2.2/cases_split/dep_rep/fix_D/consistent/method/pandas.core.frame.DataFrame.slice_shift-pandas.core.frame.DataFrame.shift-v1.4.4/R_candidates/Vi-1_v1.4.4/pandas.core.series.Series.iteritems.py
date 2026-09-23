    @Appender(items.__doc__)
    def iteritems(self) -> Iterable[tuple[Hashable, Any]]:
        return self.items()
