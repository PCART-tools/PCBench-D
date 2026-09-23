    def setup(self, fig, outfile, dpi=None):
        # docstring inherited
        super().setup(fig, outfile, dpi=dpi)
        self._w, self._h = self._adjust_frame_size()
        # Run here so that grab_frame() can write the data to a pipe. This
        # eliminates the need for temp files.
        self._run()
