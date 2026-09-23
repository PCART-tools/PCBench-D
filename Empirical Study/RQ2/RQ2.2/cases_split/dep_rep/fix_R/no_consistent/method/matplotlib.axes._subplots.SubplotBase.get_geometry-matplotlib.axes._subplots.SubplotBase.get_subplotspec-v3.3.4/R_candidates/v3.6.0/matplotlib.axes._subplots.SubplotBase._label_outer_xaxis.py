    def _label_outer_xaxis(self, *, check_patch):
        # see documentation in label_outer.
        if check_patch and not isinstance(self.patch, mpl.patches.Rectangle):
            return
        ss = self.get_subplotspec()
        label_position = self.xaxis.get_label_position()
        if not ss.is_first_row():  # Remove top label/ticklabels/offsettext.
            if label_position == "top":
                self.set_xlabel("")
            self.xaxis.set_tick_params(which="both", labeltop=False)
            if self.xaxis.offsetText.get_position()[1] == 1:
                self.xaxis.offsetText.set_visible(False)
        if not ss.is_last_row():  # Remove bottom label/ticklabels/offsettext.
            if label_position == "bottom":
                self.set_xlabel("")
            self.xaxis.set_tick_params(which="both", labelbottom=False)
            if self.xaxis.offsetText.get_position()[1] == 0:
                self.xaxis.offsetText.set_visible(False)
