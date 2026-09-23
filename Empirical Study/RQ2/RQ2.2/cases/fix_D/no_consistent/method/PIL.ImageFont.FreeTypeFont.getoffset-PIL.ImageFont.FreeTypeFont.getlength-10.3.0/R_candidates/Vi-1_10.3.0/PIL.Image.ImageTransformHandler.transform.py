    @abc.abstractmethod
    def transform(
        self,
        size: tuple[int, int],
        image: Image,
        **options: dict[str, str | int | tuple[int, ...] | list[int]],
    ) -> Image:
        pass
