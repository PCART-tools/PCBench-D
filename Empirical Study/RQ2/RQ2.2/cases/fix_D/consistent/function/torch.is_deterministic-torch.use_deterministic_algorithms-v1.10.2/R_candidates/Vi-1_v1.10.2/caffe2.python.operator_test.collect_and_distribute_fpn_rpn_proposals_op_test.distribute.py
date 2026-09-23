def distribute(rois, _, outputs, **args):
    """To understand the output blob order see return value of
    roi_data.fast_rcnn.get_fast_rcnn_blob_names(is_training=False)
    """
    # equivalent to Detectron code
    #   lvl_min = cfg.FPN.ROI_MIN_LEVEL
    #   lvl_max = cfg.FPN.ROI_MAX_LEVEL
    lvl_min = args['roi_min_level']
    lvl_max = lvl_min + args['roi_num_levels'] - 1
    lvls = map_rois_to_fpn_levels(
        rois[:, 1:5],
        lvl_min, lvl_max,
        args['roi_canonical_scale'],
        args['roi_canonical_level'])

    # equivalent to Detectron code
    #   outputs[0].reshape(rois.shape)
    #   outputs[0].data[...] = rois
    outputs[0] = rois

    # Create new roi blobs for each FPN level
    # (See: modeling.FPN.add_multilevel_roi_blobs which is similar but annoying
    # to generalize to support this particular case.)
    rois_idx_order = np.empty((0, ))
    for output_idx, lvl in enumerate(range(lvl_min, lvl_max + 1)):
        idx_lvl = np.where(lvls == lvl)[0]
        blob_roi_level = rois[idx_lvl, :]
        # equivalent to Detectron code
        #   outputs[output_idx + 1].reshape(blob_roi_level.shape)
        #   outputs[output_idx + 1].data[...] = blob_roi_level
        outputs[output_idx + 1] = blob_roi_level
        rois_idx_order = np.concatenate((rois_idx_order, idx_lvl))
    rois_idx_restore = np.argsort(rois_idx_order, kind='mergesort')
    # equivalent to Detectron code
    #   py_op_copy_blob(
    #       rois_idx_restore.astype(np.int32), outputs[-1])
    outputs[-1] = rois_idx_restore.astype(np.int32)
