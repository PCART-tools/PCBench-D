def bbox_transform_rotated(
    boxes,
    deltas,
    weights=(1.0, 1.0, 1.0, 1.0),
    angle_bound_on=True,
    angle_bound_lo=-90,
    angle_bound_hi=90,
):
    """
    Similar to bbox_transform but for rotated boxes with angle info.
    """
    if boxes.shape[0] == 0:
        return np.zeros((0, deltas.shape[1]), dtype=deltas.dtype)

    boxes = boxes.astype(deltas.dtype, copy=False)

    ctr_x = boxes[:, 0]
    ctr_y = boxes[:, 1]
    widths = boxes[:, 2]
    heights = boxes[:, 3]
    angles = boxes[:, 4]

    wx, wy, ww, wh = weights
    dx = deltas[:, 0::5] / wx
    dy = deltas[:, 1::5] / wy
    dw = deltas[:, 2::5] / ww
    dh = deltas[:, 3::5] / wh
    da = deltas[:, 4::5] * 180.0 / np.pi

    # Prevent sending too large values into np.exp()
    BBOX_XFORM_CLIP = np.log(1000. / 16.)
    dw = np.minimum(dw, BBOX_XFORM_CLIP)
    dh = np.minimum(dh, BBOX_XFORM_CLIP)

    pred_boxes = np.zeros(deltas.shape, dtype=deltas.dtype)
    pred_boxes[:, 0::5] = dx * widths[:, np.newaxis] + ctr_x[:, np.newaxis]
    pred_boxes[:, 1::5] = dy * heights[:, np.newaxis] + ctr_y[:, np.newaxis]
    pred_boxes[:, 2::5] = np.exp(dw) * widths[:, np.newaxis]
    pred_boxes[:, 3::5] = np.exp(dh) * heights[:, np.newaxis]

    pred_angle = da + angles[:, np.newaxis]
    if angle_bound_on:
        period = angle_bound_hi - angle_bound_lo
        assert period % 180 == 0
        pred_angle[np.where(pred_angle < angle_bound_lo)] += period
        pred_angle[np.where(pred_angle > angle_bound_hi)] -= period
    pred_boxes[:, 4::5] = pred_angle

    return pred_boxes
