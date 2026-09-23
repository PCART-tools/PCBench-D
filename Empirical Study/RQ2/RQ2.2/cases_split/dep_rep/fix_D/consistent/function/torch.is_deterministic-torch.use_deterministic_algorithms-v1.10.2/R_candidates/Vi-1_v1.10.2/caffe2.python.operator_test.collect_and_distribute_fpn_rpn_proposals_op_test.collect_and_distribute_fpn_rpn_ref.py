def collect_and_distribute_fpn_rpn_ref(*inputs):
    assert inputs
    args = inputs[-1]
    inputs = inputs[:-1]

    num_rpn_lvls = args['rpn_num_levels']
    assert len(inputs) == 2 * num_rpn_lvls
    N = inputs[0].shape[0]
    for i in range(num_rpn_lvls):
        assert len(inputs[i].shape) == 2
        assert inputs[i].shape[0] == N
        assert inputs[i].shape[1] == 5
    for i in range(num_rpn_lvls, 2 * num_rpn_lvls):
        assert len(inputs[i].shape) == 1
        assert inputs[i].shape[0] == N

    num_roi_lvls = args['roi_num_levels']
    outputs = (num_roi_lvls + 2) * [None]
    rois = collect(inputs, **args)
    distribute(rois, None, outputs, **args)

    return outputs
