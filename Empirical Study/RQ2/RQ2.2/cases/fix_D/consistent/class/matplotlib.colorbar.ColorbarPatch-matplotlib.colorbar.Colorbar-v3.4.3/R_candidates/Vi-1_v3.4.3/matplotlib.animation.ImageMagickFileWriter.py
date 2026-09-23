@writers.register('imagemagick_file')
class ImageMagickFileWriter(ImageMagickBase, FileMovieWriter):
    """
    File-based animated gif writer.

    Frames are written to temporary files on disk and then stitched
    together at the end.
    """

    supported_formats = ['png', 'jpeg', 'tiff', 'raw', 'rgba']

    def _args(self):
        # Force format: ImageMagick does not recognize 'raw'.
        fmt = 'rgba:' if self.frame_format == 'raw' else ''
        return ([self.bin_path(),
                 '-size', '%ix%i' % self.frame_size, '-depth', '8',
                 '-delay', str(self.delay), '-loop', '0',
                 '%s%s*.%s' % (fmt, self.temp_prefix, self.frame_format)]
                + self.output_args)
