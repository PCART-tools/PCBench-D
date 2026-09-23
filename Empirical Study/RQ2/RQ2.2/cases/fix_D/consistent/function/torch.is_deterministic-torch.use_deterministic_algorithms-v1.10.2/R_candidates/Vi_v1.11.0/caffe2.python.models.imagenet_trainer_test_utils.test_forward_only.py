def test_forward_only(
    create_model,
    last_out_blob,
    data_blob='gpu_0/data',
    num_labels=1000,
):
    model = cnn.CNNModelHelper(
        order="NCHW",
        name="test",
        cudnn_exhaustive_search=True,
    )
    with core.NameScope("gpu_0"):
            data = model.net.AddExternalInput(data_blob)
            create_model(
                model,
                data,
                num_input_channels=3,
                num_labels=num_labels,
                is_test=True
            )

    count_before = count_blobs(model.net.Proto())
    optim_proto = memonger.optimize_inference_for_dag(
        model.net, [data_blob], "gpu_0/"
    )
    count_after = count_blobs(optim_proto)
    num_shared_blobs = count_shared_blobs(optim_proto)

    # Run model and compare results
    workspace.RunNetOnce(model.param_init_net)
    data = np.random.rand(4, 3, 227, 227).astype(np.float32)

    workspace.FeedBlob(data_blob, data)
    workspace.RunNetOnce(model.net)
    model.net.Proto().type = 'dag'
    model.net.Proto().num_workers = 4
    loss1 = workspace.FetchBlob(last_out_blob)

    workspace.RunNetOnce(optim_proto)
    optimized_loss1 = workspace.FetchBlob(last_out_blob)
    return [(count_after, count_before),
            (num_shared_blobs),
            (loss1, optimized_loss1)]
