    def build_elems(self) -> None:
        from xml.etree.ElementTree import SubElement

        if not self.elem_cols:
            return

        for col in self.elem_cols:
            flat_col = col
            if isinstance(col, tuple):
                flat_col = (
                    "".join(str(c) for c in col).strip()
                    if "" in col
                    else "_".join(str(c) for c in col).strip()
                )

            elem_name = f"{self.prefix_uri}{flat_col}"
            try:
                val = (
                    None
                    if self.d[col] in [None, ""] or self.d[col] != self.d[col]
                    else str(self.d[col])
                )
                SubElement(self.elem_row, elem_name).text = val
            except KeyError:
                raise KeyError(f"no valid column, {col}")
