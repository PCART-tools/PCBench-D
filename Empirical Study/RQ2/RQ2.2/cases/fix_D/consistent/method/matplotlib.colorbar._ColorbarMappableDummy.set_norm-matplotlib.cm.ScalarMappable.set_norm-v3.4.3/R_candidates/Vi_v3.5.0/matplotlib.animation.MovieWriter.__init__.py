    def __init__(self, fps=5, codec=None, bitrate=None, extra_args=None,
                 metadata=None):
        """
        Parameters
        ----------
        fps : int, default: 5
            Movie frame rate (per second).
        codec : str or None, default: :rc:`animation.codec`
            The codec to use.
        bitrate : int, default: :rc:`animation.bitrate`
            The bitrate of the movie, in kilobits per second.  Higher values
            means higher quality movies, but increase the file size.  A value
            of -1 lets the underlying movie encoder select the bitrate.
        extra_args : list of str or None, optional
            Extra command-line arguments passed to the underlying movie
            encoder.  The default, None, means to use
            :rc:`animation.[name-of-encoder]_args` for the builtin writers.
        metadata : dict[str, str], default: {}
            A dictionary of keys and values for metadata to include in the
            output file. Some keys that may be of use include:
            title, artist, genre, subject, copyright, srcform, comment.
        """
        if type(self) is MovieWriter:
            # TODO MovieWriter is still an abstract class and needs to be
            #      extended with a mixin. This should be clearer in naming
            #      and description. For now, just give a reasonable error
            #      message to users.
            raise TypeError(
                'MovieWriter cannot be instantiated directly. Please use one '
                'of its subclasses.')

        super().__init__(fps=fps, metadata=metadata, codec=codec,
                         bitrate=bitrate)
        self.frame_format = self.supported_formats[0]
        self.extra_args = extra_args
