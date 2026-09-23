def test_shared_grads(
    with_shapes,
    create_model,
    conv_blob,
    last_out_blob,
    data_blob='gpu_0/data',
    label_blob='gpu_0/label',
    num_labels=1000,
):
    model = cnn.CNNModelHelper(
        order="NCHW",
        name="test",
        cudnn_exhaustive_search=True,
    )
    with core.NameScope("gpu_0"):
        data = model.net.AddExternalInput(data_blob)
        label = model.net.AddExternalInput(label_blob)
        (_softmax, loss) = create_model(
            model,
            data,
            num_input_channels=3,
            num_labels=num_labels,
            label=label,
            is_test=False,
        )

    param_to_grad = model.AddGradientOperators([loss])

    (shapes, types) = workspace.InferShapesAndTypes(
        [model.param_init_net, model.net],
        {data_blob: [4, 3, 227, 227],
         label_blob: [4]},
    )

    count_before = count_blobs(model.net.Proto())
    optim_proto = memonger.share_grad_blobs(
        model.net,
        ["gpu_0/loss"],
        set(model.param_to_grad.values()),
        "gpu_0/",
        share_activations=True,
        dont_share_blobs=set([str(param_to_grad[conv_blob])]),
        blob_shapes=shapes if with_shapes else None,
    )
    count_after = count_blobs(optim_proto)

    # Run model and compare results. We check that the loss is same
    # and also that the final gradient (conv1_w_grad is same)
    workspace.RunNetOnce(model.param_init_net)
    data = np.random.rand(4, 3, 227, 227).astype(np.float32)
    label = (np.random.rand(4) * num_labels).astype(np.int32)

    workspace.FeedBlob(data_blob, data)
    workspace.FeedBlob(label_blob, label)

    workspace.RunNetOnce(model.net)
    model.net.Proto().type = 'dag'
    model.net.Proto().num_workers = 4
    loss1 = workspace.FetchBlob(last_out_blob)
    conv1_w_grad = workspace.FetchBlob(param_to_grad[conv_blob])
    workspace.FeedBlob(param_to_grad[conv_blob], np.array([0.0]))

    workspace.RunNetOnce(optim_proto)
    optimized_loss1 = workspace.FetchBlob(last_out_blob)
    optim_conv1_w_grad = workspace.FetchBlob(param_to_grad[conv_blob])

    return [(count_after, count_before),
            (loss1, optimized_loss1),
            (conv1_w_grad, optim_conv1_w_grad)]
