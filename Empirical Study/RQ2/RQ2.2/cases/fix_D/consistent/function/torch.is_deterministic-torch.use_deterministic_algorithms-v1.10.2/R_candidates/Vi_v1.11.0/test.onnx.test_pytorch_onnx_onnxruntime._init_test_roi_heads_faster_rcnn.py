def _init_test_roi_heads_faster_rcnn():
    out_channels = 256
    num_classes = 91

    box_fg_iou_thresh = 0.5
    box_bg_iou_thresh = 0.5
    box_batch_size_per_image = 512
    box_positive_fraction = 0.25
    bbox_reg_weights = None
    box_score_thresh = 0.05
    box_nms_thresh = 0.5
    box_detections_per_img = 100

    box_roi_pool = ops.MultiScaleRoIAlign(
        featmap_names=["0", "1", "2", "3"],
        output_size=7,
        sampling_ratio=2)

    resolution = box_roi_pool.output_size[0]
    representation_size = 1024
    box_head = TwoMLPHead(
        out_channels * resolution ** 2,
        representation_size)

    representation_size = 1024
    box_predictor = FastRCNNPredictor(
        representation_size,
        num_classes)

    roi_heads = RoIHeads(
        box_roi_pool, box_head, box_predictor,
        box_fg_iou_thresh, box_bg_iou_thresh,
        box_batch_size_per_image, box_positive_fraction,
        bbox_reg_weights,
        box_score_thresh, box_nms_thresh, box_detections_per_img)
    return roi_heads
