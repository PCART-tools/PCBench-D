@writers.register('avconv')
class AVConvWriter(AVConvBase, FFMpegWriter):
    """
    Pipe-based avconv writer.

    Frames are streamed directly to avconv via a pipe and written in a single
    pass.
    """
