    def _translate_body(self, idx_lengths: dict, max_rows: int, max_cols: int):
        """
        Build each <tr> within table <body> as a list

        Use the following structure:
          +--------------------------------------------+---------------------------+
          |  index_header_0    ...    index_header_n   |  data_by_column   ...     |
          +--------------------------------------------+---------------------------+

        Also add elements to the cellstyle_map for more efficient grouped elements in
        <style></style> block

        Parameters
        ----------
        sparsify_index : bool
            Whether index_headers section will add rowspan attributes (>1) to elements.

        Returns
        -------
        body : list
            The associated HTML elements needed for template rendering.
        """
        rlabels = self.data.index.tolist()
        if not isinstance(self.data.index, MultiIndex):
            rlabels = [[x] for x in rlabels]

        body, row_count = [], 0
        for r, row_tup in [
            z for z in enumerate(self.data.itertuples()) if z[0] not in self.hidden_rows
        ]:
            row_count += 1
            if row_count > max_rows:  # used only to add a '...' trimmed row:
                trimmed_row = self._generate_trimmed_row(max_cols)
                body.append(trimmed_row)
                break
            body_row = self._generate_body_row(
                (r, row_tup, rlabels), max_cols, idx_lengths
            )
            body.append(body_row)
        return body
