    def to_jshtml(self, fps=None, embed_frames=True, default_mode=None):
        """Generate HTML representation of the animation"""
        if fps is None and hasattr(self, '_interval'):
            # Convert interval in ms to frames per second
            fps = 1000 / self._interval

        # If we're not given a default mode, choose one base on the value of
        # the repeat attribute
        if default_mode is None:
            default_mode = 'loop' if self.repeat else 'once'

        if hasattr(self, "_html_representation"):
            return self._html_representation
        else:
            # Can't open a second time while opened on windows. So we avoid
            # deleting when closed, and delete manually later.
            with tempfile.NamedTemporaryFile(suffix='.html',
                                             delete=False) as f:
                self.save(f.name, writer=HTMLWriter(fps=fps,
                                                    embed_frames=embed_frames,
                                                    default_mode=default_mode))
            # Re-open and get content
            with open(f.name) as fobj:
                html = fobj.read()

            # Now we can delete
            os.remove(f.name)

            self._html_representation = html
            return html
