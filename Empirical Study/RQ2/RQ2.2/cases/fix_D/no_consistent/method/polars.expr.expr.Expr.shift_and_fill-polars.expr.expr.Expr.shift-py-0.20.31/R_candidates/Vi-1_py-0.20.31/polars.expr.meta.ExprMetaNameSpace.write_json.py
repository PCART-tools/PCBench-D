    @deprecate_renamed_function("Expr.meta.serialize", version="0.20.11")
    def write_json(self, file: IOBase | str | Path | None = None) -> str | None:
        """
        Write expression to json.

        .. deprecated:: 0.20.11
            This method has been renamed to :meth:`serialize`.
        """
        return self.serialize(file)
