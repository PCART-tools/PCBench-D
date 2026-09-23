def distribute_fpn_ref(*inputs):
    args = inputs[-1]
    inputs = inputs[:-1]
    rois = inputs[0]
    num_roi_lvls = args['roi_num_levels']
    outputs = (num_roi_lvls + 2) * [None]
    distribute(rois, None, outputs, **args)
    # remove the first rois from output of distribute
    outputs.pop(0)
    return outputs
