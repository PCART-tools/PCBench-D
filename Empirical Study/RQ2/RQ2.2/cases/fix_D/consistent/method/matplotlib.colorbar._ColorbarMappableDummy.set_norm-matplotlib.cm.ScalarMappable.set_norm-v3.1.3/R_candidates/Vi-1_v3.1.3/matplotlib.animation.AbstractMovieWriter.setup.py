    @abc.abstractmethod
    def setup(self, fig, outfile, dpi=None):
        '''
        Perform setup for writing the movie file.

        Parameters
        ----------
        fig : `~matplotlib.figure.Figure`
            The figure object that contains the information for frames
        outfile : string
            The filename of the resulting movie file
        dpi : int, optional
            The DPI (or resolution) for the file.  This controls the size
            in pixels of the resulting movie file. Default is ``fig.dpi``.
        '''
