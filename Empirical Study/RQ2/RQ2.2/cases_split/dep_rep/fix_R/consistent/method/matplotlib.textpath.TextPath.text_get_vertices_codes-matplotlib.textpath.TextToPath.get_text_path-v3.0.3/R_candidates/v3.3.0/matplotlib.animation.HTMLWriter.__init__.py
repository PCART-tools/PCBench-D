    def __init__(self, fps=30, codec=None, bitrate=None, extra_args=None,
                 metadata=None, embed_frames=False, default_mode='loop',
                 embed_limit=None):

        if extra_args:
            _log.warning("HTMLWriter ignores 'extra_args'")
        extra_args = ()  # Don't lookup nonexistent rcParam[args_key].
        self.embed_frames = embed_frames
        self.default_mode = default_mode.lower()
        cbook._check_in_list(['loop', 'once', 'reflect'],
                             default_mode=self.default_mode)

        # Save embed limit, which is given in MB
        if embed_limit is None:
            self._bytes_limit = mpl.rcParams['animation.embed_limit']
        else:
            self._bytes_limit = embed_limit
        # Convert from MB to bytes
        self._bytes_limit *= 1024 * 1024

        super().__init__(fps, codec, bitrate, extra_args, metadata)
