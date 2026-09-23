    def _label_outer_yaxis(self, *, skip_non_rectangular_axes,
                           remove_inner_ticks=False):
        # see documentation in label_outer.
        if skip_non_rectangular_axes and not isinstance(self.patch,
                                                        mpl.patches.Rectangle):
            return
        ss = self.get_subplotspec()
        if not ss:
            return
        label_position = self.yaxis.get_label_position()
        if not ss.is_first_col():  # Remove left label/ticklabels/offsettext.
            if label_position == "left":
                self.set_ylabel("")
            left_kw = {'left': False} if remove_inner_ticks else {}
            self.yaxis.set_tick_params(
                which="both", labelleft=False, **left_kw)
            if self.yaxis.offsetText.get_position()[0] == 0:
                self.yaxis.offsetText.set_visible(False)
        if not ss.is_last_col():  # Remove right label/ticklabels/offsettext.
            if label_position == "right":
                self.set_ylabel("")
            right_kw = {'right': False} if remove_inner_ticks else {}
            self.yaxis.set_tick_params(
                which="both", labelright=False, **right_kw)
            if self.yaxis.offsetText.get_position()[0] == 1:
                self.yaxis.offsetText.set_visible(False)
