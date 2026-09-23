    def grab_frame(self, **savefig_kwargs):
        '''
        Grab the image information from the figure and save as a movie frame.

        All keyword arguments in savefig_kwargs are passed on to the `savefig`
        command that saves the figure.
        '''
        _log.debug('MovieWriter.grab_frame: Grabbing frame.')
        # re-adjust the figure size in case it has been changed by the
        # user.  We must ensure that every frame is the same size or
        # the movie will not save correctly.
        self.fig.set_size_inches(self._w, self._h)
        # Tell the figure to save its data to the sink, using the
        # frame format and dpi.
        self.fig.savefig(self._frame_sink(), format=self.frame_format,
                         dpi=self.dpi, **savefig_kwargs)
