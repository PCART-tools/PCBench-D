    def __init__(self, fps=5, codec=None, bitrate=None, extra_args=None,
                 metadata=None):
        '''MovieWriter

        Parameters
        ----------
        fps: int
            Framerate for movie.
        codec: string or None, optional
            The codec to use. If ``None`` (the default) the ``animation.codec``
            rcParam is used.
        bitrate: int or None, optional
            The bitrate for the saved movie file, which is one way to control
            the output file size and quality. The default value is ``None``,
            which uses the ``animation.bitrate`` rcParam.  A value of -1
            implies that the bitrate should be determined automatically by the
            underlying utility.
        extra_args: list of strings or None, optional
            A list of extra string arguments to be passed to the underlying
            movie utility. The default is ``None``, which passes the additional
            arguments in the ``animation.extra_args`` rcParam.
        metadata: Dict[str, str] or None
            A dictionary of keys and values for metadata to include in the
            output file. Some keys that may be of use include:
            title, artist, genre, subject, copyright, srcform, comment.
        '''
        self.fps = fps
        self.frame_format = 'rgba'

        if codec is None:
            self.codec = rcParams['animation.codec']
        else:
            self.codec = codec

        if bitrate is None:
            self.bitrate = rcParams['animation.bitrate']
        else:
            self.bitrate = bitrate

        if extra_args is None:
            self.extra_args = list(rcParams[self.args_key])
        else:
            self.extra_args = extra_args

        if metadata is None:
            self.metadata = dict()
        else:
            self.metadata = metadata
