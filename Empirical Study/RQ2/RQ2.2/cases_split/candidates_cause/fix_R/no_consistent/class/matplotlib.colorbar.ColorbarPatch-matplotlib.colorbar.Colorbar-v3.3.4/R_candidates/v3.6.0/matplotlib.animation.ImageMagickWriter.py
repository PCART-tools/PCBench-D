@writers.register('imagemagick')
class ImageMagickWriter(ImageMagickBase, MovieWriter):
    """
    Pipe-based animated gif.

    Frames are streamed directly to ImageMagick via a pipe and written
    in a single pass.
    """

    input_names = "-"  # stdin
