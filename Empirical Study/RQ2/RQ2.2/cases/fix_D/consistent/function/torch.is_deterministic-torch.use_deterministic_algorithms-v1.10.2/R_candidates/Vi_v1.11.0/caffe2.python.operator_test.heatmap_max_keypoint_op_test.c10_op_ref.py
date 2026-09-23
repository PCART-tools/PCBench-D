def c10_op_ref(maps, rois):
    keypoints = torch.ops._caffe2.HeatmapMaxKeypoint(
        torch.tensor(maps),
        torch.tensor(rois),
        should_output_softmax=True,
    )
    return [keypoints.numpy()]
