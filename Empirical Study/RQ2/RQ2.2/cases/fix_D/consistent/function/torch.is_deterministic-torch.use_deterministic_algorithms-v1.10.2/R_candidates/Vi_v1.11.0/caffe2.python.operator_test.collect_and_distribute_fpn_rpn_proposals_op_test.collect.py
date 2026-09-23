def collect(inputs, **args):
    post_nms_topN = args['rpn_post_nms_topN']
    num_lvls = args['rpn_num_levels']
    roi_inputs = inputs[:num_lvls]
    score_inputs = inputs[num_lvls:]

    # rois are in [[batch_idx, x0, y0, x1, y2], ...] format
    # Combine predictions across all levels and retain the top scoring
    #
    # equivalent to Detectron code
    #   rois = np.concatenate([blob.data for blob in roi_inputs])
    #   scores = np.concatenate([blob.data for blob in score_inputs]).squeeze()
    rois = np.concatenate(roi_inputs)
    scores = np.concatenate(score_inputs).squeeze()
    assert rois.shape[0] == scores.shape[0]
    inds = np.argsort(-scores, kind='mergesort')[:post_nms_topN]
    rois = rois[inds, :]
    return rois
