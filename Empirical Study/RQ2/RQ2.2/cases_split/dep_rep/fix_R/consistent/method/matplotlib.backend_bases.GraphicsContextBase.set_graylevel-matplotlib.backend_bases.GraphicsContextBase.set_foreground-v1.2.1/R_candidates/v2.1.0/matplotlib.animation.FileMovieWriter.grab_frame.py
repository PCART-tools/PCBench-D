    def grab_frame(self, **savefig_kwargs):
        '''
        Grab the image information from the figure and save as a movie frame.
        All keyword arguments in savefig_kwargs are passed on to the `savefig`
        command that saves the figure.
        '''
        # Overloaded to explicitly close temp file.
        verbose.report('MovieWriter.grab_frame: Grabbing frame.',
                       level='debug')
        try:
            # Tell the figure to save its data to the sink, using the
            # frame format and dpi.
            with self._frame_sink() as myframesink:
                self.fig.savefig(myframesink, format=self.frame_format,
                                 dpi=self.dpi, **savefig_kwargs)

        except RuntimeError:
            out, err = self._proc.communicate()
            verbose.report('MovieWriter -- Error '
                           'running proc:\n%s\n%s' % (out,
                                                      err), level='helpful')
            raise
