@_api.deprecated('3.3')
class AVConvBase(FFMpegBase):
    """
    Mixin class for avconv output.

    To be useful this must be multiply-inherited from with a
    `MovieWriterBase` sub-class.
    """

    _exec_key = 'animation.avconv_path'
    _args_key = 'animation.avconv_args'

    # NOTE : should be removed when the same method is removed in FFMpegBase.
    isAvailable = classmethod(MovieWriter.isAvailable.__func__)
