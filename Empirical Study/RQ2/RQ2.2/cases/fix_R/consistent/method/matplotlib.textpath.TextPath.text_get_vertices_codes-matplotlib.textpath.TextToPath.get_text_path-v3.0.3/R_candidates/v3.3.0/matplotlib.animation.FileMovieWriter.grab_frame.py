    def grab_frame(self, **savefig_kwargs):
        # docstring inherited
        # Overloaded to explicitly close temp file.
        _log.debug('MovieWriter.grab_frame: Grabbing frame.')
        # Tell the figure to save its data to the sink, using the
        # frame format and dpi.
        with self._frame_sink() as myframesink:
            self.fig.savefig(myframesink, format=self.frame_format,
                             dpi=self.dpi, **savefig_kwargs)
