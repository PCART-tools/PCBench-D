def prelu(model, blob_in, blob_out, num_channels=1, slope_init=None,
          **kwargs):
    """PRelu"""
    slope_init = (
        slope_init if slope_init else ('ConstantFill', {'value': 0.25}))
    if model.init_params:
        slope = model.param_init_net.__getattr__(slope_init[0])(
            [],
            blob_out + '_slope',
            shape=[num_channels],
            **slope_init[1]
        )
    else:
        slope = core.ScopedBlobReference(
            blob_out + '_slope', model.param_init_net)

    model.AddParameter(slope)

    return model.net.PRelu([blob_in, slope], [blob_out])
