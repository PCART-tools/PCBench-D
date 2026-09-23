    def _update_ctx(self, attrs: DataFrame) -> None:
        """
        Update the state of the ``Styler`` for data cells.

        Collects a mapping of {index_label: [('<property>', '<value>'), ..]}.

        Parameters
        ----------
        attrs : DataFrame
            should contain strings of '<property>: <value>;<prop2>: <val2>'
            Whitespace shouldn't matter and the final trailing ';' shouldn't
            matter.
        """
        if not self.index.is_unique or not self.columns.is_unique:
            raise KeyError(
                "`Styler.apply` and `.applymap` are not compatible "
                "with non-unique index or columns."
            )

        for cn in attrs.columns:
            j = self.columns.get_loc(cn)
            ser = attrs[cn]
            for rn, c in ser.items():
                if not c or pd.isna(c):
                    continue
                css_list = maybe_convert_css_to_tuples(c)
                i = self.index.get_loc(rn)
                self.ctx[(i, j)].extend(css_list)
