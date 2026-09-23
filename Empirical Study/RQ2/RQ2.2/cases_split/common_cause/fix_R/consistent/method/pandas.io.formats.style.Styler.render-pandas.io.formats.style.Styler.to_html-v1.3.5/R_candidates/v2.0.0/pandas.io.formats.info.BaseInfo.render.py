    @abstractmethod
    def render(
        self,
        *,
        buf: WriteBuffer[str] | None,
        max_cols: int | None,
        verbose: bool | None,
        show_counts: bool | None,
    ) -> None:
        pass
