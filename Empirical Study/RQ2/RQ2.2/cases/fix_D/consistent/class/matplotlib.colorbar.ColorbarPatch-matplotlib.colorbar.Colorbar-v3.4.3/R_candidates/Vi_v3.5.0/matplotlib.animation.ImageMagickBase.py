class ImageMagickBase:
    """
    Mixin class for ImageMagick output.

    To be useful this must be multiply-inherited from with a
    `MovieWriterBase` sub-class.
    """

    _exec_key = 'animation.convert_path'
    _args_key = 'animation.convert_args'

    @property
    def delay(self):
        return 100. / self.fps

    @property
    def output_args(self):
        extra_args = (self.extra_args if self.extra_args is not None
                      else mpl.rcParams[self._args_key])
        return [*extra_args, self.outfile]

    @classmethod
    def bin_path(cls):
        binpath = super().bin_path()
        if binpath == 'convert':
            binpath = mpl._get_executable_info('magick').executable
        return binpath

    @classmethod
    def isAvailable(cls):
        try:
            return super().isAvailable()
        except mpl.ExecutableNotFoundError as _enf:
            # May be raised by get_executable_info.
            _log.debug('ImageMagick unavailable due to: %s', _enf)
            return False
