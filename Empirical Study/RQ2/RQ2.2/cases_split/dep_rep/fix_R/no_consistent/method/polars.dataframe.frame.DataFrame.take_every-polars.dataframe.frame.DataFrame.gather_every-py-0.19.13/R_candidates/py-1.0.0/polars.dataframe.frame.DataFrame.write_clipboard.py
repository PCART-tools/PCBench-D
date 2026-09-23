    def write_clipboard(self, *, separator: str = "\t", **kwargs: Any) -> None:
        """
        Copy `DataFrame` in csv format to the system clipboard with `write_csv`.

        Useful for pasting into Excel or other similar spreadsheet software.

        Parameters
        ----------
        separator
            Separate CSV fields with this symbol.
        kwargs
            Additional arguments to pass to `write_csv`.

        See Also
        --------
        polars.read_clipboard: Read a DataFrame from the clipboard.
        write_csv: Write to comma-separated values (CSV) file.
        """
        result: str = self.write_csv(file=None, separator=separator, **kwargs)
        _write_clipboard_string(result)
