    def _label_outer_xaxis(self, *, skip_non_rectangular_axes,
                           remove_inner_ticks=False):
        # see documentation in label_outer.
        if skip_non_rectangular_axes and not isinstance(self.patch,
                                                        mpl.patches.Rectangle):
            return
        ss = self.get_subplotspec()
        if not ss:
            return
        label_position = self.xaxis.get_label_position()
        if not ss.is_first_row():  # Remove top label/ticklabels/offsettext.
            if label_position == "top":
                self.set_xlabel("")
            top_kw = {'top': False} if remove_inner_ticks else {}
            self.xaxis.set_tick_params(
                which="both", labeltop=False, **top_kw)
            if self.xaxis.offsetText.get_position()[1] == 1:
                self.xaxis.offsetText.set_visible(False)
        if not ss.is_last_row():  # Remove bottom label/ticklabels/offsettext.
            if label_position == "bottom":
                self.set_xlabel("")
            bottom_kw = {'bottom': False} if remove_inner_ticks else {}
            self.xaxis.set_tick_params(
                which="both", labelbottom=False, **bottom_kw)
            if self.xaxis.offsetText.get_position()[1] == 0:
                self.xaxis.offsetText.set_visible(False)
