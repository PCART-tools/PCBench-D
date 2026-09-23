@writers.register('imagemagick_file')
class ImageMagickFileWriter(ImageMagickBase, FileMovieWriter):
    """
    File-based animated gif writer.

    Frames are written to temporary files on disk and then stitched
    together at the end.
    """

    supported_formats = ['png', 'jpeg', 'tiff', 'raw', 'rgba']
    input_names = property(
        lambda self: f'{self.temp_prefix}*.{self.frame_format}')
