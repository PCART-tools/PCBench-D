    def _join_multiline(self, *strcols):
        lwidth = self.line_width
        adjoin_width = 1
        strcols = list(strcols)
        if self.index:
            idx = strcols.pop(0)
            lwidth -= np.array([len(x) for x in idx]).max() + adjoin_width

        col_widths = [np.array([len(x) for x in col]).max()
                      if len(col) > 0 else 0
                      for col in strcols]
        col_bins = _binify(col_widths, lwidth)
        nbins = len(col_bins)

        if self.max_rows and len(self.frame) > self.max_rows:
            nrows = self.max_rows + 1
        else:
            nrows = len(self.frame)

        str_lst = []
        st = 0
        for i, ed in enumerate(col_bins):
            row = strcols[st:ed]
            row.insert(0, idx)
            if nbins > 1:
                if ed <= len(strcols) and i < nbins - 1:
                    row.append([' \\'] + ['  '] * (nrows - 1))
                else:
                    row.append([' '] * nrows)

            str_lst.append(adjoin(adjoin_width, *row))
            st = ed
        return '\n\n'.join(str_lst)
