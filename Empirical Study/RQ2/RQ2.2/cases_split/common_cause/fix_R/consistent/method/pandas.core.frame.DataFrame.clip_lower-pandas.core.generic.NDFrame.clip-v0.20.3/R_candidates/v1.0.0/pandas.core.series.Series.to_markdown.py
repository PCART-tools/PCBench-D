    @Appender(
        """
        Examples
        --------
        >>> s = pd.Series(["elk", "pig", "dog", "quetzal"], name="animal")
        >>> print(s.to_markdown())
        |    | animal   |
        |---:|:---------|
        |  0 | elk      |
        |  1 | pig      |
        |  2 | dog      |
        |  3 | quetzal  |
        """
    )
    @Substitution(klass="Series")
    @Appender(generic._shared_docs["to_markdown"])
    def to_markdown(
        self, buf: Optional[IO[str]] = None, mode: Optional[str] = None, **kwargs
    ) -> Optional[str]:
        return self.to_frame().to_markdown(buf, mode, **kwargs)
