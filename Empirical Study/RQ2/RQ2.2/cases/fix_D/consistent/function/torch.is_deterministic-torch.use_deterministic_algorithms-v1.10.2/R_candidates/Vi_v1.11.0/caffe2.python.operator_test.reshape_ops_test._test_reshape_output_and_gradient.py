def _test_reshape_output_and_gradient(
    old_shape,
    new_shape,
    expected_shape=None,
    arg_shape=True,
    in_place=False,
    expected_gradient=None
):
    devices = [core.DeviceOption(caffe2_pb2.CPU, 0)]
    if workspace.NumGpuDevices() > 0:
        devices.append(core.DeviceOption(workspace.GpuDeviceType, 0))

    for device_opt in devices:
        with core.DeviceScope(device_opt):
            if expected_shape is None:
                expected_shape = new_shape
            net = core.Net('net')

            if len(old_shape) == 0:
                # scalar, convert to tensor before feeding to blob
                X = np.atleast_1d(np.random.rand(*old_shape))
            else:
                X = np.random.rand(*old_shape).astype(np.float32)
            blob_in = 'X'
            blob_out = blob_in if in_place else blob_in + '_out'

            if arg_shape:
                out, _ = net.Reshape([blob_in], [blob_out, 'old_shape'], shape=new_shape)
            else:
                out, _ = net.Reshape([blob_in, 'new_shape'], [blob_out, 'old_shape'])
                workspace.FeedBlob('new_shape', np.asarray(new_shape))

            workspace.FeedBlob(blob_in, X)
            if expected_gradient is not None:
                net.AddGradientOperators([out])
            workspace.CreateNet(net)
            workspace.RunNetOnce(net)

            Y = workspace.FetchBlob(blob_out)
            np.testing.assert_allclose(Y, X.reshape(expected_shape))
            if expected_gradient is not None:
                data_grad = workspace.FetchBlob(blob_in + '_grad')
                np.testing.assert_array_equal(data_grad, expected_gradient)
