def collect_rpn_ref(*inputs):
    args = inputs[-1]
    inputs = inputs[:-1]
    rois = collect(inputs, **args)
    return [rois]
