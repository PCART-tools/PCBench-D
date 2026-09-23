    def _auto_set_font_size(self, renderer):

        if len(self._cells) == 0:
            return
        fontsize = list(six.itervalues(self._cells))[0].get_fontsize()
        cells = []
        for key, cell in six.iteritems(self._cells):
            # ignore auto-sized columns
            if key[1] in self._autoColumns:
                continue
            size = cell.auto_set_font_size(renderer)
            fontsize = min(fontsize, size)
            cells.append(cell)

        # now set all fontsizes equal
        for cell in six.itervalues(self._cells):
            cell.set_fontsize(fontsize)
