    @abc.abstractmethod
    def transform(
        self,
        size: tuple[int, int],
        image: Image,
        **options: Any,
    ) -> Image:
        pass
