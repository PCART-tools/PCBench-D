    def build_attribs(self, d: dict[str, Any], elem_row: Any) -> Any:
        """
        Create attributes of row.

        This method adds attributes using attr_cols to row element and
        works with tuples for multindex or hierarchical columns.
        """

        if not self.attr_cols:
            return elem_row

        for col in self.attr_cols:
            attr_name = self._get_flat_col_name(col)
            try:
                if not isna(d[col]):
                    elem_row.attrib[attr_name] = str(d[col])
            except KeyError:
                raise KeyError(f"no valid column, {col}")
        return elem_row
