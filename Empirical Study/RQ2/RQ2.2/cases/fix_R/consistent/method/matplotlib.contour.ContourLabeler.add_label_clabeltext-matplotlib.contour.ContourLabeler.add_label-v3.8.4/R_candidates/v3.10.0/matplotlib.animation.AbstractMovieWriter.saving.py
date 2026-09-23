    @contextlib.contextmanager
    def saving(self, fig, outfile, dpi, *args, **kwargs):
        """
        Context manager to facilitate writing the movie file.

        ``*args, **kw`` are any parameters that should be passed to `setup`.
        """
        if mpl.rcParams['savefig.bbox'] == 'tight':
            _log.info("Disabling savefig.bbox = 'tight', as it may cause "
                      "frame size to vary, which is inappropriate for "
                      "animation.")

        # This particular sequence is what contextlib.contextmanager wants
        self.setup(fig, outfile, dpi, *args, **kwargs)
        with mpl.rc_context({'savefig.bbox': None}):
            try:
                yield self
            finally:
                self.finish()
