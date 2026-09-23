    def grab_frame(self, **savefig_kwargs):
        # docstring inherited
        _validate_grabframe_kwargs(savefig_kwargs)
        _log.debug('MovieWriter.grab_frame: Grabbing frame.')
        # Readjust the figure size in case it has been changed by the user.
        # All frames must have the same size to save the movie correctly.
        self.fig.set_size_inches(self._w, self._h)
        # Save the figure data to the sink, using the frame format and dpi.
        self.fig.savefig(self._proc.stdin, format=self.frame_format,
                         dpi=self.dpi, **savefig_kwargs)
