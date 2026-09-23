    def _update_ctx_header(self, attrs: DataFrame, axis: int) -> None:
        """
        Update the state of the ``Styler`` for header cells.

        Collects a mapping of {index_label: [('<property>', '<value>'), ..]}.

        Parameters
        ----------
        attrs : Series
            Should contain strings of '<property>: <value>;<prop2>: <val2>', and an
            integer index.
            Whitespace shouldn't matter and the final trailing ';' shouldn't
            matter.
        axis : int
            Identifies whether the ctx object being updated is the index or columns
        """
        for j in attrs.columns:
            ser = attrs[j]
            for i, c in ser.items():
                if not c:
                    continue
                css_list = maybe_convert_css_to_tuples(c)
                if axis == 0:
                    self.ctx_index[(i, j)].extend(css_list)
                else:
                    self.ctx_columns[(j, i)].extend(css_list)
