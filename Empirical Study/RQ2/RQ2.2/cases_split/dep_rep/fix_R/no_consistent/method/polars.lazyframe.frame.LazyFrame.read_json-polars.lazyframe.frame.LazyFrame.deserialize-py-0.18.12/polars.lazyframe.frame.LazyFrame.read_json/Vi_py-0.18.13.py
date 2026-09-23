    @classmethod
    @deprecate_renamed_function("deserialize", version="0.18.12")
    @deprecate_renamed_parameter("file", "source", version="0.18.12")
    def read_json(cls, source: str | Path | IOBase) -> Self:
        """
        Read a logical plan from a JSON file to construct a LazyFrame.

        .. deprecated:: 0.18.12
            This class method has been renamed to ``deserialize``.

        Parameters
        ----------
        source
            Path to a file or a file-like object.

        See Also
        --------
        deserialize

        """
        return cls.deserialize(source)
