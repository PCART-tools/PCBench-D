def _resample(
        image_obj, data, out_shape, transform, *, resample=None, alpha=1):
    """
    Convenience wrapper around `._image.resample` to resample *data* to
    *out_shape* (with a third dimension if *data* is RGBA) that takes care of
    allocating the output array and fetching the relevant properties from the
    Image object *image_obj*.
    """

    # decide if we need to apply anti-aliasing if the data is upsampled:
    # compare the number of displayed pixels to the number of
    # the data pixels.
    interpolation = image_obj.get_interpolation()
    if interpolation == 'antialiased':
        # don't antialias if upsampling by an integer number or
        # if zooming in more than a factor of 3
        pos = np.array([[0, 0], [data.shape[1], data.shape[0]]])
        disp = transform.transform(pos)
        dispx = np.abs(np.diff(disp[:, 0]))
        dispy = np.abs(np.diff(disp[:, 1]))
        if ((dispx > 3 * data.shape[1] or
                dispx == data.shape[1] or
                dispx == 2 * data.shape[1]) and
            (dispy > 3 * data.shape[0] or
                dispy == data.shape[0] or
                dispy == 2 * data.shape[0])):
            interpolation = 'nearest'
        else:
            interpolation = 'hanning'
    out = np.zeros(out_shape + data.shape[2:], data.dtype)  # 2D->2D, 3D->3D.
    if resample is None:
        resample = image_obj.get_resample()
    _image.resample(data, out, transform,
                    _interpd_[interpolation],
                    resample,
                    alpha,
                    image_obj.get_filternorm(),
                    image_obj.get_filterrad())
    return out
