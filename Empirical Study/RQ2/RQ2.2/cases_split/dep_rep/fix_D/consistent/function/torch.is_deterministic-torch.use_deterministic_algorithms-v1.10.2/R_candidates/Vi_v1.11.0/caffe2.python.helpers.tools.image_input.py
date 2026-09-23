def image_input(
    model, blob_in, blob_out, order="NCHW", use_gpu_transform=False, **kwargs
):
    assert 'is_test' in kwargs, "Argument 'is_test' is required"
    if order == "NCHW":
        if (use_gpu_transform):
            kwargs['use_gpu_transform'] = 1 if use_gpu_transform else 0
            # GPU transform will handle NHWC -> NCHW
            outputs = model.net.ImageInput(blob_in, blob_out, **kwargs)
            pass
        else:
            outputs = model.net.ImageInput(
                blob_in, [blob_out[0] + '_nhwc'] + blob_out[1:], **kwargs
            )
            outputs_list = list(outputs)
            outputs_list[0] = model.net.NHWC2NCHW(outputs_list[0], blob_out[0])
            outputs = tuple(outputs_list)
    else:
        outputs = model.net.ImageInput(blob_in, blob_out, **kwargs)
    return outputs
