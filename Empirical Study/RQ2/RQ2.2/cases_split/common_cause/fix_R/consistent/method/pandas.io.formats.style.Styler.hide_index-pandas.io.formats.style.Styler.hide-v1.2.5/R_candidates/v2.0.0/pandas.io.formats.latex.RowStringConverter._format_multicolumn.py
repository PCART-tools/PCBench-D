    def _format_multicolumn(self, row: list[str]) -> list[str]:
        r"""
        Combine columns belonging to a group to a single multicolumn entry
        according to self.multicolumn_format

        e.g.:
        a &  &  & b & c &
        will become
        \multicolumn{3}{l}{a} & b & \multicolumn{2}{l}{c}
        """
        row2 = row[: self.index_levels]
        ncol = 1
        coltext = ""

        def append_col() -> None:
            # write multicolumn if needed
            if ncol > 1:
                row2.append(
                    f"\\multicolumn{{{ncol:d}}}{{{self.multicolumn_format}}}"
                    f"{{{coltext.strip()}}}"
                )
            # don't modify where not needed
            else:
                row2.append(coltext)

        for c in row[self.index_levels :]:
            # if next col has text, write the previous
            if c.strip():
                if coltext:
                    append_col()
                coltext = c
                ncol = 1
            # if not, add it to the previous multicolumn
            else:
                ncol += 1
        # write last column name
        if coltext:
            append_col()
        return row2
