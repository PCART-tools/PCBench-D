    def _update_title_position(self, renderer):
        """
        Update the title position based on the bounding box enclosing
        all the ticklabels and x-axis spine and xlabel...
        """
        _log.debug('update_title_pos')

        if self._autotitlepos is not None and not self._autotitlepos:
            _log.debug('title position was updated manually, not adjusting')
            return

        titles = (self.title, self._left_title, self._right_title)

        if self._autotitlepos is None:
            for title in titles:
                x, y = title.get_position()
                if not np.isclose(y, 1.0):
                    self._autotitlepos = False
                    _log.debug('not adjusting title pos because title was'
                             ' already placed manually: %f', y)
                    return
            self._autotitlepos = True

        for title in titles:
            x, y0 = title.get_position()
            y = 1.0
            # need to check all our twins too...
            axs = self._twinned_axes.get_siblings(self)

            for ax in axs:
                try:
                    if (ax.xaxis.get_label_position() == 'top'
                            or ax.xaxis.get_ticks_position() == 'top'):
                        bb = ax.xaxis.get_tightbbox(renderer)
                        top = bb.ymax
                        # we don't need to pad because the padding is already
                        # in __init__: titleOffsetTrans
                        yn = self.transAxes.inverted().transform((0., top))[1]
                        y = max(y, yn)
                except AttributeError:
                    pass

            title.set_position((x, y))
