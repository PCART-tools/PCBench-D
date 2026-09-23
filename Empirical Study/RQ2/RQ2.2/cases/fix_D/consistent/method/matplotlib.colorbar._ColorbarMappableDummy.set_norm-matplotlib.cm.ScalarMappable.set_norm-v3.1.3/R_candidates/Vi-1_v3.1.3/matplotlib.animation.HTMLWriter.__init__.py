    def __init__(self, fps=30, codec=None, bitrate=None, extra_args=None,
                 metadata=None, embed_frames=False, default_mode='loop',
                 embed_limit=None):
        self.embed_frames = embed_frames
        self.default_mode = default_mode.lower()

        # Save embed limit, which is given in MB
        if embed_limit is None:
            self._bytes_limit = rcParams['animation.embed_limit']
        else:
            self._bytes_limit = embed_limit

        # Convert from MB to bytes
        self._bytes_limit *= 1024 * 1024

        if self.default_mode not in ['loop', 'once', 'reflect']:
            raise ValueError(
                "unrecognized default_mode {!r}".format(self.default_mode))

        super().__init__(fps, codec, bitrate, extra_args, metadata)
