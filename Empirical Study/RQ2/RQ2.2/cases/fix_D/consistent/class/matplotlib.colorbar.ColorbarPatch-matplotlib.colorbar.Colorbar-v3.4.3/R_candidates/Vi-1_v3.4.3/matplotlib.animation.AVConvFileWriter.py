@writers.register('avconv_file')
class AVConvFileWriter(AVConvBase, FFMpegFileWriter):
    """
    File-based avconv writer.

    Frames are written to temporary files on disk and then stitched
    together at the end.
    """
