    def setup(self, fig, outfile, dpi, frame_dir=None):
        root, ext = os.path.splitext(outfile)
        if ext not in ['.html', '.htm']:
            raise ValueError("outfile must be *.htm or *.html")

        self._saved_frames = []
        self._total_bytes = 0
        self._hit_limit = False

        if not self.embed_frames:
            if frame_dir is None:
                frame_dir = root + '_frames'
            if not os.path.exists(frame_dir):
                os.makedirs(frame_dir)
            frame_prefix = os.path.join(frame_dir, 'frame')
        else:
            frame_prefix = None

        super().setup(fig, outfile, dpi, frame_prefix, clear_temp=False)
