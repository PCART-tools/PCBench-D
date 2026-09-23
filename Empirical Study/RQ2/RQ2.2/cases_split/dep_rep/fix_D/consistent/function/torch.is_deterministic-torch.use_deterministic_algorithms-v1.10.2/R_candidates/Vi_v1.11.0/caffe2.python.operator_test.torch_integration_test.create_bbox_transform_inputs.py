def create_bbox_transform_inputs(roi_counts, num_classes, rotated):
    batch_size = len(roi_counts)
    total_rois = sum(roi_counts)
    im_dims = np.random.randint(100, 600, batch_size)
    rois = (
        generate_rois_rotated(roi_counts, im_dims)
        if rotated
        else generate_rois(roi_counts, im_dims)
    )
    box_dim = 5 if rotated else 4
    deltas = np.random.randn(total_rois, box_dim * num_classes).astype(np.float32)
    im_info = np.zeros((batch_size, 3)).astype(np.float32)
    im_info[:, 0] = im_dims
    im_info[:, 1] = im_dims
    im_info[:, 2] = 1.0
    return rois, deltas, im_info
