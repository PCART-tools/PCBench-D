    def setup(self, fig, outfile, dpi, frame_dir=None):
        if os.path.splitext(outfile)[-1] not in ['.html', '.htm']:
            raise ValueError("outfile must be *.htm or *.html")

        if not self.embed_frames:
            if frame_dir is None:
                frame_dir = outfile.rstrip('.html') + '_frames'
            if not os.path.exists(frame_dir):
                os.makedirs(frame_dir)
            frame_prefix = os.path.join(frame_dir, 'frame')
        else:
            frame_prefix = None

        super(HTMLWriter, self).setup(fig, outfile, dpi,
                                      frame_prefix, clear_temp=False)
