def gen_multiple_boxes(centers, scores, count, num_classes):
    ret_box = None
    ret_scores = None
    for cc, ss in zip(centers, scores):
        box = gen_boxes(count, cc)
        ret_box = np.vstack((ret_box, box)) if ret_box is not None else box
        cur_sc = np.ones((count, 1), dtype=np.float32) * ss
        ret_scores = np.vstack((ret_scores, cur_sc)) \
            if ret_scores is not None else cur_sc
    ret_box = np.tile(ret_box, (1, num_classes))
    ret_scores = np.tile(ret_scores, (1, num_classes))
    assert ret_box.shape == (len(centers) * count, 4 * num_classes)
    assert ret_scores.shape == (len(centers) * count, num_classes)
    return ret_box, ret_scores
