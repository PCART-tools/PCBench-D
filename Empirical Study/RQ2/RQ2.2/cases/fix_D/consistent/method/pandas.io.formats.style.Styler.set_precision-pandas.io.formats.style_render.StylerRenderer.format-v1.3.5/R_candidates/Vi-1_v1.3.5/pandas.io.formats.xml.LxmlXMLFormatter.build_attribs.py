    def build_attribs(self) -> None:
        if not self.attr_cols:
            return

        for col in self.attr_cols:
            flat_col = col
            if isinstance(col, tuple):
                flat_col = (
                    "".join(str(c) for c in col).strip()
                    if "" in col
                    else "_".join(str(c) for c in col).strip()
                )

            attr_name = f"{self.prefix_uri}{flat_col}"
            try:
                val = (
                    None
                    if self.d[col] is None or self.d[col] != self.d[col]
                    else str(self.d[col])
                )
                if val is not None:
                    self.elem_row.attrib[attr_name] = val
            except KeyError:
                raise KeyError(f"no valid column, {col}")
