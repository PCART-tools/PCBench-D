def AddImageInput(
    model,
    reader,
    batch_size,
    img_size,
    dtype,
    is_test,
    mean_per_channel=None,
    std_per_channel=None,
):
    '''
    The image input operator loads image and label data from the reader and
    applies transformations to the images (random cropping, mirroring, ...).
    '''
    data, label = brew.image_input(
        model,
        reader, ["data", "label"],
        batch_size=batch_size,
        output_type=dtype,
        use_gpu_transform=True if core.IsGPUDeviceType(model._device_type) else False,
        use_caffe_datum=True,
        mean_per_channel=mean_per_channel,
        std_per_channel=std_per_channel,
        # mean_per_channel takes precedence over mean
        mean=128.,
        std=128.,
        scale=256,
        crop=img_size,
        mirror=1,
        is_test=is_test,
    )

    data = model.StopGradient(data, data)
