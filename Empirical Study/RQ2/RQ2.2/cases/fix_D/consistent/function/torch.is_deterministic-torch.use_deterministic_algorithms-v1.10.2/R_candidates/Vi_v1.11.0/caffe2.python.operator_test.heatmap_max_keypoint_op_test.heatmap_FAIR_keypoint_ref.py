def heatmap_FAIR_keypoint_ref(maps, rois):
    return [keypoint_utils.heatmaps_to_keypoints(maps, rois)]
