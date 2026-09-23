    @abstractmethod
    def get_chunks(self, n_chunks: int | None = None) -> Iterable[Column]:
        """
        Return an iterator yielding the chunks.

        See `DataFrame.get_chunks` for details on ``n_chunks``.
        """
