    @Appender(
        """
        Examples
        --------
        >>> df = pd.DataFrame(
        ...     data={"animal_1": ["elk", "pig"], "animal_2": ["dog", "quetzal"]}
        ... )
        >>> print(df.to_markdown())
        |    | animal_1   | animal_2   |
        |---:|:-----------|:-----------|
        |  0 | elk        | dog        |
        |  1 | pig        | quetzal    |
        """
    )
    @Substitution(klass="DataFrame")
    @Appender(_shared_docs["to_markdown"])
    def to_markdown(
        self, buf: Optional[IO[str]] = None, mode: Optional[str] = None, **kwargs
    ) -> Optional[str]:
        kwargs.setdefault("headers", "keys")
        kwargs.setdefault("tablefmt", "pipe")
        tabulate = import_optional_dependency("tabulate")
        result = tabulate.tabulate(self, **kwargs)
        if buf is None:
            return result
        buf, _, _, _ = get_filepath_or_buffer(buf, mode=mode)
        assert buf is not None  # Help mypy.
        buf.writelines(result)
        return None
