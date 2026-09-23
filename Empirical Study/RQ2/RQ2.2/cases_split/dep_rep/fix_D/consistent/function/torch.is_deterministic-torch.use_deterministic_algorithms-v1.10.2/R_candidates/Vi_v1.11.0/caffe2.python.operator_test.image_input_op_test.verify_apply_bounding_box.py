def verify_apply_bounding_box(img, box):
    import skimage.util
    if any(type(box[f]) is not int or np.isnan(box[f] or box[f] < 0)
           for f in range(0, 4)):
        return img
    # Box is ymin, xmin, bound_height, bound_width
    y_bounds = (box[0], img.shape[0] - box[0] - box[2])
    x_bounds = (box[1], img.shape[1] - box[1] - box[3])
    c_bounds = (0, 0)

    if any(el < 0 for el in list(y_bounds) + list(x_bounds) + list(c_bounds)):
        return img

    bboxed = skimage.util.crop(img, (y_bounds, x_bounds, c_bounds))
    return bboxed
