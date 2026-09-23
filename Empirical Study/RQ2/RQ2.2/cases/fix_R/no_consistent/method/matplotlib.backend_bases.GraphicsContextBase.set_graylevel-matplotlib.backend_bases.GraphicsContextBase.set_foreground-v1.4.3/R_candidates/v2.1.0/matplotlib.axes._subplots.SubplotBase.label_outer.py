    def label_outer(self):
        """Only show "outer" labels and tick labels.

        x-labels are only kept for subplots on the last row; y-labels only for
        subplots on the first column.
        """
        lastrow = self.is_last_row()
        firstcol = self.is_first_col()
        if not lastrow:
            for label in self.get_xticklabels(which="both"):
                label.set_visible(False)
            self.get_xaxis().get_offset_text().set_visible(False)
            self.set_xlabel("")
        if not firstcol:
            for label in self.get_yticklabels(which="both"):
                label.set_visible(False)
            self.get_yaxis().get_offset_text().set_visible(False)
            self.set_ylabel("")
