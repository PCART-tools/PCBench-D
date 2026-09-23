    def label_outer(self):
        """
        Only show "outer" labels and tick labels.

        x-labels are only kept for subplots on the last row; y-labels only for
        subplots on the first column.
        """
        ss = self.get_subplotspec()
        lastrow = ss.is_last_row()
        firstcol = ss.is_first_col()
        if not lastrow:
            for label in self.get_xticklabels(which="both"):
                label.set_visible(False)
            self.xaxis.get_offset_text().set_visible(False)
            self.set_xlabel("")
        if not firstcol:
            for label in self.get_yticklabels(which="both"):
                label.set_visible(False)
            self.yaxis.get_offset_text().set_visible(False)
            self.set_ylabel("")
