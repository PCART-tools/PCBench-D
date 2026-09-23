def verify_crop(img, crop):
    import skimage.util
    assert img.shape[0] >= crop
    assert img.shape[1] >= crop
    y_offset = 0
    if img.shape[0] > crop:
        y_offset = (img.shape[0] - crop) // 2

    x_offset = 0
    if img.shape[1] > crop:
        x_offset = (img.shape[1] - crop) // 2

    y_bounds = (y_offset, img.shape[0] - crop - y_offset)
    x_bounds = (x_offset, img.shape[1] - crop - x_offset)
    c_bounds = (0, 0)
    cropped = skimage.util.crop(img, (y_bounds, x_bounds, c_bounds))
    assert cropped.shape[0] == crop
    assert cropped.shape[1] == crop
    return cropped
