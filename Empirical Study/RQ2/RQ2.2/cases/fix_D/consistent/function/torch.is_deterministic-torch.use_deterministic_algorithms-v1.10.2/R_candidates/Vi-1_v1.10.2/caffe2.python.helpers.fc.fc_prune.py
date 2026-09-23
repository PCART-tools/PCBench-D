def fc_prune(
    model, blob_in, blob_out, dim_in, dim_out,
    weight_init=None, bias_init=None, mask_init=None,
    threshold=0.00001, need_compress_rate=False,
    comp_lb=0.05,
    **kwargs
):
    """FC_Prune version
    Runnable so far. Great!:)
    """
    weight_init = weight_init if weight_init else ('XavierFill', {})
    bias_init = bias_init if bias_init else ('ConstantFill', {})
    mask_init = mask_init if mask_init else ('ConstantFill', {})
    blob_out = blob_out or model.net.NextName()
    compress_rate = blob_out + '_compress_rate'
    if model.init_params:
        compress_lb = model.param_init_net.ConstantFill(
            [],
            blob_out + '_lb',
            shape=[1],
            value=comp_lb
        )
        weight = model.param_init_net.__getattr__(weight_init[0])(
            [],
            blob_out + '_w',
            shape=[dim_out, dim_in],
            **weight_init[1]
        )
        mask = model.param_init_net.ConstantFill(
            [],
            blob_out + '_m',
            shape=[dim_out, dim_in],
            value=1.0
        )
        ag_dw = model.param_init_net.__getattr__(mask_init[0])(
            [],
            blob_out + '_ag_dw',
            shape=[dim_out, dim_in],
            **mask_init[1]
        )
        bias = model.param_init_net.__getattr__(bias_init[0])(
            [],
            blob_out + '_b',
            shape=[dim_out, ],
            **bias_init[1]
        )
        mask_seq = model.param_init_net.__getattr__(mask_init[0])(
            [],
            blob_out + '_mask_seq',
            shape=[dim_out, dim_in],
            **mask_init[1]
        )
        thres = model.param_init_net.ConstantFill(
            [],
            blob_out + '_thres',
            shape=[1],
            value=threshold
        )
    else:
        compress_lb = core.ScopedBlobReference(
            blob_out + '_lb', model.param_init_net)
        weight = core.ScopedBlobReference(
            blob_out + '_w', model.param_init_net)
        bias = core.ScopedBlobReference(
            blob_out + '_b', model.param_init_net)
        mask = core.ScopedBlobReference(
            blob_out + '_m', model.param_init_net)
        ag_dw = core.ScopedBlobReference(
            blob_out + '_ag_dw', model.param_init_net)
        mask_seq = core.ScopedBlobReference(
            blob_out + '_mask_seq', model.param_init_net)
        thres = core.ScopedBlobReference(
            blob_out + '_thres', model.param_init_net)

    model.AddParameter(weight)
    model.AddParameter(bias)
    if need_compress_rate:
        return model.net.FC_Prune([blob_in, weight, mask, bias, ag_dw, mask_seq,
                                   thres, compress_lb],
                                  [blob_out, compress_rate], **kwargs)
    else:
        return model.net.FC_Prune([blob_in, weight, mask,
                                   bias, ag_dw, mask_seq,
                                   thres, compress_lb],
                                  blob_out, **kwargs)
