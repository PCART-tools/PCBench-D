    def to_jshtml(self, fps=None, embed_frames=True, default_mode=None):
        """Generate HTML representation of the animation"""
        if fps is None and hasattr(self, '_interval'):
            # Convert interval in ms to frames per second
            fps = 1000 / self._interval

        # If we're not given a default mode, choose one base on the value of
        # the repeat attribute
        if default_mode is None:
            default_mode = 'loop' if self.repeat else 'once'

        if not hasattr(self, "_html_representation"):
            # Can't open a NamedTemporaryFile twice on Windows, so use a
            # TemporaryDirectory instead.
            with TemporaryDirectory() as tmpdir:
                path = Path(tmpdir, "temp.html")
                writer = HTMLWriter(fps=fps,
                                    embed_frames=embed_frames,
                                    default_mode=default_mode)
                self.save(str(path), writer=writer)
                self._html_representation = path.read_text()

        return self._html_representation
