    def write_header(self) -> None:
        """Write the header of an HTML table."""
        with Tag(self.elements, "thead"):
            if not bool(int(os.environ.get("POLARS_FMT_TABLE_HIDE_COLUMN_NAMES", "0"))):
                with Tag(self.elements, "tr"):
                    columns = self.df.columns
                    for c in self.col_idx:
                        with Tag(self.elements, "th"):
                            if c == -1:
                                self.elements.append("&hellip;")
                            else:
                                self.elements.append(html.escape(columns[c]))
            if not bool(
                int(os.environ.get("POLARS_FMT_TABLE_HIDE_COLUMN_DATA_TYPES", "0"))
            ):
                with Tag(self.elements, "tr"):
                    dtypes = self.df._df.dtype_strings()
                    for c in self.col_idx:
                        with Tag(self.elements, "td"):
                            if c == -1:
                                self.elements.append("&hellip;")
                            else:
                                self.elements.append(dtypes[c])
