    def _translate_latex(self, d: dict) -> None:
        r"""
        Post-process the default render dict for the LaTeX template format.

        Processing items included are:
          - Remove hidden columns from the non-headers part of the body.
          - Place cellstyles directly in td cells rather than use cellstyle_map.
          - Remove hidden indexes or reinsert missing th elements if part of multiindex
            or multirow sparsification (so that \multirow and \multicol work correctly).
        """
        d["head"] = [[col for col in row if col["is_visible"]] for row in d["head"]]
        body = []
        for r, row in enumerate(d["body"]):
            if self.hide_index_:
                row_body_headers = []
            else:
                row_body_headers = [
                    {
                        **col,
                        "display_value": col["display_value"]
                        if col["is_visible"]
                        else "",
                    }
                    for col in row
                    if col["type"] == "th"
                ]

            row_body_cells = [
                {**col, "cellstyle": self.ctx[r, c - self.data.index.nlevels]}
                for c, col in enumerate(row)
                if (col["is_visible"] and col["type"] == "td")
            ]

            body.append(row_body_headers + row_body_cells)
        d["body"] = body
