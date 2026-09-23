    def setup(self, fig, outfile, dpi=None):
        '''
        Perform setup for writing the movie file.

        Parameters
        ----------
        fig : matplotlib.figure.Figure
            The figure object that contains the information for frames
        outfile : string
            The filename of the resulting movie file
        dpi : int, optional
            The DPI (or resolution) for the file.  This controls the size
            in pixels of the resulting movie file. Default is fig.dpi.
        '''
        self.outfile = outfile
        self.fig = fig
        if dpi is None:
            dpi = self.fig.dpi
        self.dpi = dpi
        self._w, self._h = self._adjust_frame_size()

        # Run here so that grab_frame() can write the data to a pipe. This
        # eliminates the need for temp files.
        self._run()
