    @doc(
        Series.to_markdown,
        klass=_shared_doc_kwargs["klass"],
        storage_options=_shared_docs["storage_options"],
        examples="""Examples
        --------
        >>> df = pd.DataFrame(
        ...     data={"animal_1": ["elk", "pig"], "animal_2": ["dog", "quetzal"]}
        ... )
        >>> print(df.to_markdown())
        |    | animal_1   | animal_2   |
        |---:|:-----------|:-----------|
        |  0 | elk        | dog        |
        |  1 | pig        | quetzal    |

        Output markdown with a tabulate option.

        >>> print(df.to_markdown(tablefmt="grid"))
        +----+------------+------------+
        |    | animal_1   | animal_2   |
        +====+============+============+
        |  0 | elk        | dog        |
        +----+------------+------------+
        |  1 | pig        | quetzal    |
        +----+------------+------------+""",
    )
    def to_markdown(
        self,
        buf: FilePath | WriteBuffer[str] | None = None,
        mode: str = "wt",
        index: bool = True,
        storage_options: StorageOptions = None,
        **kwargs,
    ) -> str | None:
        if "showindex" in kwargs:
            warnings.warn(
                "'showindex' is deprecated. Only 'index' will be used "
                "in a future version. Use 'index' to silence this warning.",
                FutureWarning,
                stacklevel=find_stack_level(inspect.currentframe()),
            )

        kwargs.setdefault("headers", "keys")
        kwargs.setdefault("tablefmt", "pipe")
        kwargs.setdefault("showindex", index)
        tabulate = import_optional_dependency("tabulate")
        result = tabulate.tabulate(self, **kwargs)
        if buf is None:
            return result

        with get_handle(buf, mode, storage_options=storage_options) as handles:
            handles.handle.write(result)
        return None
