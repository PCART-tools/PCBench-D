    def render(self) -> list[str]:
        """Return the lines needed to render a HTML table."""
        if not bool(
            int(
                os.environ.get("POLARS_FMT_TABLE_HIDE_DATAFRAME_SHAPE_INFORMATION", "0")
            )
        ):
            # format frame/series shape with '_' thousand-separators
            s = self.df.shape
            shape = f"({s[0]:_},)" if self.from_series else f"({s[0]:_}, {s[1]:_})"

            self.elements.append(f"<small>shape: {shape}</small>")

        with Tag(
            # be careful changing the CSS class ref here...
            # ref: https://github.com/pola-rs/polars/issues/7443
            self.elements,
            "table",
            {"border": "1", "class": "dataframe"},
        ):
            self.write_header()
            self.write_body()
        return self.elements
