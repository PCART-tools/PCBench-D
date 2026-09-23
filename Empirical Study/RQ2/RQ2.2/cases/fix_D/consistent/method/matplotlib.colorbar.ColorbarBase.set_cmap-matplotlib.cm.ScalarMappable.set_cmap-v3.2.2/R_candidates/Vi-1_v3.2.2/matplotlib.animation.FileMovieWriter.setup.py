    def setup(self, fig, outfile, dpi=None, frame_prefix='_tmp',
              clear_temp=True):
        '''Perform setup for writing the movie file.

        Parameters
        ----------
        fig : `~matplotlib.figure.Figure`
            The figure to grab the rendered frames from.
        outfile : str
            The filename of the resulting movie file.
        dpi : number, optional
            The dpi of the output file. This, with the figure size,
            controls the size in pixels of the resulting movie file.
            Default is fig.dpi.
        frame_prefix : str, optional
            The filename prefix to use for temporary files.  Defaults to
            ``'_tmp'``.
        clear_temp : bool, optional
            If the temporary files should be deleted after stitching
            the final result.  Setting this to ``False`` can be useful for
            debugging.  Defaults to ``True``.

        '''
        self.fig = fig
        self.outfile = outfile
        if dpi is None:
            dpi = self.fig.dpi
        self.dpi = dpi
        self._adjust_frame_size()

        self.clear_temp = clear_temp
        self.temp_prefix = frame_prefix
        self._frame_counter = 0  # used for generating sequential file names
        self._temp_paths = list()
        self.fname_format_str = '%s%%07d.%s'
