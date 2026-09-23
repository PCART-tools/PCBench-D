    def to_latex(
        self,
        buf: FilePath | WriteBuffer[str] | None = None,
        column_format: str | None = None,
        longtable: bool = False,
        encoding: str | None = None,
        multicolumn: bool = False,
        multicolumn_format: str | None = None,
        multirow: bool = False,
        caption: str | tuple[str, str] | None = None,
        label: str | None = None,
        position: str | None = None,
    ) -> str | None:
        """
        Render a DataFrame to a LaTeX tabular/longtable environment output.
        """
        from pandas.io.formats.latex import LatexFormatter

        latex_formatter = LatexFormatter(
            self.fmt,
            longtable=longtable,
            column_format=column_format,
            multicolumn=multicolumn,
            multicolumn_format=multicolumn_format,
            multirow=multirow,
            caption=caption,
            label=label,
            position=position,
        )
        string = latex_formatter.to_string()
        return save_to_buffer(string, buf=buf, encoding=encoding)
