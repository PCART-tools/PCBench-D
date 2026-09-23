def map_rois_to_fpn_levels(
    rois,
    k_min, k_max,
    roi_canonical_scale, roi_canonical_level
):
    """Determine which FPN level each RoI in a set of RoIs should map to based
    on the heuristic in the FPN paper.
    """
    # Compute level ids
    s = np.sqrt(boxes_area(rois))

    # Eqn.(1) in FPN paper
    target_lvls = np.floor(
        roi_canonical_level +
        np.log2(s / roi_canonical_scale + 1e-6))
    target_lvls = np.clip(target_lvls, k_min, k_max)
    return target_lvls
