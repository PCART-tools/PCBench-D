def clip_tiled_boxes_rotated(boxes, im_shape, angle_thresh=1.0):
    """
    Similar to clip_tiled_boxes but for rotated boxes with angle info.
    Only clips almost horizontal boxes within angle_thresh. The rest are
    left unchanged.
    """
    assert (
        boxes.shape[1] % 5 == 0
    ), "boxes.shape[1] is {:d}, but must be divisible by 5.".format(
        boxes.shape[1]
    )

    (H, W) = im_shape[:2]

    # Filter boxes that are almost upright within angle_thresh tolerance
    idx = np.where(np.abs(boxes[:, 4::5]) <= angle_thresh)
    idx5 = idx[1] * 5
    # convert to (x1, y1, x2, y2)
    x1 = boxes[idx[0], idx5] - (boxes[idx[0], idx5 + 2] - 1) / 2.0
    y1 = boxes[idx[0], idx5 + 1] - (boxes[idx[0], idx5 + 3] - 1) / 2.0
    x2 = boxes[idx[0], idx5] + (boxes[idx[0], idx5 + 2] - 1) / 2.0
    y2 = boxes[idx[0], idx5 + 1] + (boxes[idx[0], idx5 + 3] - 1) / 2.0
    # clip
    x1 = np.maximum(np.minimum(x1, W - 1), 0)
    y1 = np.maximum(np.minimum(y1, H - 1), 0)
    x2 = np.maximum(np.minimum(x2, W - 1), 0)
    y2 = np.maximum(np.minimum(y2, H - 1), 0)
    # convert back to (xc, yc, w, h)
    boxes[idx[0], idx5] = (x1 + x2) / 2.0
    boxes[idx[0], idx5 + 1] = (y1 + y2) / 2.0
    boxes[idx[0], idx5 + 2] = x2 - x1 + 1
    boxes[idx[0], idx5 + 3] = y2 - y1 + 1

    return boxes
