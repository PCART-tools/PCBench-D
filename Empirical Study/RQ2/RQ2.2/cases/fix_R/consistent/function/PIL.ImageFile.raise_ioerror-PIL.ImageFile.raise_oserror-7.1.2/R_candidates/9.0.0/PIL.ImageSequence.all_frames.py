def all_frames(im, func=None):
    """
    Applies a given function to all frames in an image or a list of images.
    The frames are returned as a list of separate images.

    :param im: An image, or a list of images.
    :param func: The function to apply to all of the image frames.
    :returns: A list of images.
    """
    if not isinstance(im, list):
        im = [im]

    ims = []
    for imSequence in im:
        current = imSequence.tell()

        ims += [im_frame.copy() for im_frame in Iterator(imSequence)]

        imSequence.seek(current)
    return [func(im) for im in ims] if func else ims
