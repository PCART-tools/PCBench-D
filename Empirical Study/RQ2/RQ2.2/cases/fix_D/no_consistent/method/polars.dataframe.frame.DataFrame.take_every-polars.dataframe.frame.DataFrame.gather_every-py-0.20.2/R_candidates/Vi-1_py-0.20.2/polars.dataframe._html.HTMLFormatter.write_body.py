    def write_body(self) -> None:
        """Write the body of an HTML table."""
        str_lengths = int(os.environ.get("POLARS_FMT_STR_LEN", "15"))
        with Tag(self.elements, "tbody"):
            for r in self.row_idx:
                with Tag(self.elements, "tr"):
                    for c in self.col_idx:
                        with Tag(self.elements, "td"):
                            if r == -1 or c == -1:
                                self.elements.append("&hellip;")
                            else:
                                series = self.df[:, c]
                                self.elements.append(
                                    html.escape(series._s.get_fmt(r, str_lengths))
                                )
