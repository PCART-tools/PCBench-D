    def __iter__(self) -> typing.Iterator[str]:
        return (cookie.name for cookie in self.jar)
