    @property
    @abc.abstractmethod
    def series_generator(self) -> Iterator["Series"]:
        pass
