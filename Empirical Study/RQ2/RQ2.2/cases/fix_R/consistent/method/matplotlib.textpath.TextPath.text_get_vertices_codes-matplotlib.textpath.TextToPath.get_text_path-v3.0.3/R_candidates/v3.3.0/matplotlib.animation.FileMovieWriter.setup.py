    @cbook._delete_parameter("3.3", "clear_temp")
    def setup(self, fig, outfile, dpi=None, frame_prefix=None,
              clear_temp=True):
        """
        Setup for writing the movie file.

        Parameters
        ----------
        fig : `~matplotlib.figure.Figure`
            The figure to grab the rendered frames from.
        outfile : str
            The filename of the resulting movie file.
        dpi : float, optional
            The dpi of the output file. This, with the figure size,
            controls the size in pixels of the resulting movie file.
            Default is ``fig.dpi``.
        frame_prefix : str, optional
            The filename prefix to use for temporary files.  If None (the
            default), files are written to a temporary directory which is
            deleted by `cleanup` (regardless of the value of *clear_temp*).
        clear_temp : bool, optional
            If the temporary files should be deleted after stitching
            the final result.  Setting this to ``False`` can be useful for
            debugging.  Defaults to ``True``.
        """
        self.fig = fig
        self.outfile = outfile
        if dpi is None:
            dpi = self.fig.dpi
        self.dpi = dpi
        self._adjust_frame_size()

        if frame_prefix is None:
            self._tmpdir = TemporaryDirectory()
            self.temp_prefix = str(Path(self._tmpdir.name, 'tmp'))
        else:
            self._tmpdir = None
            self.temp_prefix = frame_prefix
        self._clear_temp = clear_temp
        self._frame_counter = 0  # used for generating sequential file names
        self._temp_paths = list()
        self.fname_format_str = '%s%%07d.%s'
