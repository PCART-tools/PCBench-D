def instance_norm(model, blob_in, blob_out, dim_in, order="NCHW", **kwargs):
    blob_out = blob_out or model.net.NextName()
    # Input: input, scale, bias
    # Output: output, saved_mean, saved_inv_std
    # scale: initialize with ones
    # bias: initialize with zeros

    def init_blob(value, suffix):
        return model.param_init_net.ConstantFill(
            [], blob_out + "_" + suffix, shape=[dim_in], value=value)
    scale, bias = init_blob(1.0, "s"), init_blob(0.0, "b")

    model.AddParameter(scale, ParameterTags.WEIGHT)
    model.AddParameter(bias, ParameterTags.BIAS)
    blob_outs = [blob_out, blob_out + "_sm", blob_out + "_siv"]
    if 'is_test' in kwargs and kwargs['is_test']:
        blob_outputs = model.net.InstanceNorm(
            [blob_in, scale, bias], [blob_out],
            order=order, **kwargs)
        return blob_outputs
    else:
        blob_outputs = model.net.InstanceNorm(
            [blob_in, scale, bias], blob_outs,
            order=order, **kwargs)
        # Return the output
        return blob_outputs[0]
