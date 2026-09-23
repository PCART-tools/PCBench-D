    def _build_elems(self, sub_element_cls, d: dict[str, Any], elem_row: Any) -> None:
        if not self.elem_cols:
            return

        for col in self.elem_cols:
            elem_name = self._get_flat_col_name(col)
            try:
                val = None if isna(d[col]) or d[col] == "" else str(d[col])
                sub_element_cls(elem_row, elem_name).text = val
            except KeyError:
                raise KeyError(f"no valid column, {col}")
