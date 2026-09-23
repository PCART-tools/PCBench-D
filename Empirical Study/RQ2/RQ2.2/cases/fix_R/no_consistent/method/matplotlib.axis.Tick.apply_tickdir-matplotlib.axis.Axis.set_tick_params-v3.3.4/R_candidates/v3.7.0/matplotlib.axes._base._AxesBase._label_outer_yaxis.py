    def _label_outer_yaxis(self, *, check_patch):
        # see documentation in label_outer.
        if check_patch and not isinstance(self.patch, mpl.patches.Rectangle):
            return
        ss = self.get_subplotspec()
        if not ss:
            return
        label_position = self.yaxis.get_label_position()
        if not ss.is_first_col():  # Remove left label/ticklabels/offsettext.
            if label_position == "left":
                self.set_ylabel("")
            self.yaxis.set_tick_params(which="both", labelleft=False)
            if self.yaxis.offsetText.get_position()[0] == 0:
                self.yaxis.offsetText.set_visible(False)
        if not ss.is_last_col():  # Remove right label/ticklabels/offsettext.
            if label_position == "right":
                self.set_ylabel("")
            self.yaxis.set_tick_params(which="both", labelright=False)
            if self.yaxis.offsetText.get_position()[0] == 1:
                self.yaxis.offsetText.set_visible(False)
